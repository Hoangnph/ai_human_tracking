"""Module quản lý danh tính của đối tượng được theo dõi.

Module này cung cấp các lớp và hàm để kết hợp thông tin từ object tracking
và face recognition, duy trì danh tính của đối tượng qua thời gian.

Examples:
    >>> from src.tracking.identity_tracker import TrackedPerson, IdentityTracker
    >>> identity_tracker = IdentityTracker()
    >>> # Cập nhật danh tính
    >>> identity_tracker.update_identities(tracks, face_identities)
"""

from typing import Dict, List, Optional, Tuple, Union, Any
import numpy as np
import time
from dataclasses import dataclass, field
from enum import Enum
import cv2

from src.face_recognition.face_database import FaceIdentity
from src.constants import IdentityType
from src.utils.logger import logger


class IdentityConfidenceLevel(Enum):
    """Các mức độ tin cậy của danh tính."""
    
    UNKNOWN = 0  # Chưa xác định
    LOW = 1      # Độ tin cậy thấp
    MEDIUM = 2   # Độ tin cậy trung bình
    HIGH = 3     # Độ tin cậy cao
    VERY_HIGH = 4  # Độ tin cậy rất cao


@dataclass
class IdentityMatch:
    """Lưu trữ kết quả nhận diện khuôn mặt."""
    
    identity: FaceIdentity  # Danh tính nhận diện được
    similarity: float       # Độ tương đồng (0-1)
    frame_number: int       # Frame nhận diện
    timestamp: float = field(default_factory=time.time)  # Thời điểm nhận diện


class TrackedPerson:
    """Quản lý danh tính của một đối tượng đang được theo dõi.

    Lớp này duy trì danh tính của một người qua thời gian, 
    kết hợp thông tin từ nhiều lần nhận diện để đưa ra danh tính ổn định.

    Attributes:
        track_id: ID đối tượng đang theo dõi
        identity_matches: Lịch sử các lần nhận diện
        current_identity: Danh tính hiện tại của đối tượng
        confidence_level: Mức độ tin cậy về danh tính
        confidence_score: Điểm tin cậy (0-100)
        last_match_frame: Frame cuối cùng có nhận diện
        last_face_match_frame: Frame cuối cùng có khuôn mặt
        total_tracked_frames: Tổng số frame đã theo dõi
        face_detected_frames: Số frame đã phát hiện khuôn mặt
    """

    def __init__(self, track_id: int):
        """Khởi tạo đối tượng theo dõi danh tính.

        Args:
            track_id: ID đối tượng đang theo dõi
        """
        self.track_id = track_id
        self.identity_matches: List[IdentityMatch] = []
        self.current_identity: Optional[FaceIdentity] = None
        self.confidence_level = IdentityConfidenceLevel.UNKNOWN
        self.confidence_score = 0.0  # 0-100
        self.last_match_frame = -1
        self.last_face_match_frame = -1  # Frame cuối cùng có khuôn mặt
        self.total_tracked_frames = 0
        self.face_detected_frames = 0
        self._identity_scores: Dict[str, float] = {}  # Điểm cho mỗi danh tính

    def update(self, has_face_match: bool = False, current_frame: int = None) -> None:
        """Cập nhật trạng thái của đối tượng theo dõi.

        Args:
            has_face_match: Có phải frame hiện tại có khuôn mặt không
            current_frame: Số frame hiện tại
        """
        if current_frame is not None:
            self.total_tracked_frames += 1
            
            # Cập nhật frame cuối cùng
            self.last_match_frame = current_frame
            
            # Cập nhật trạng thái khuôn mặt
            if has_face_match:
                self.last_face_match_frame = current_frame
                
            # Giảm điểm tin cậy theo thời gian nếu không có nhận diện mới
            frames_since_last_face = current_frame - self.last_face_match_frame if self.last_face_match_frame >= 0 else 0
            if frames_since_last_face > 30:  # Sau 30 frame không có nhận diện khuôn mặt mới
                self._decay_confidence()

    def add_identity_match(
        self, 
        identity: Any, 
        similarity: float, 
        current_frame: int
    ) -> None:
        """Thêm kết quả nhận diện mới.

        Args:
            identity: Danh tính nhận diện được
            similarity: Độ tương đồng (0-1)
            current_frame: Số thứ tự frame hiện tại
        """
        # Debug thông tin về identity
        logger.info(f"add_identity_match: identity type = {type(identity)}, value = {identity}")
        
        # Chuyển đổi similarity (0-1) sang confidence score (0-100)
        confidence_score = similarity * 100
        
        # Nếu không có danh tính, không cần làm gì
        if identity is None or identity == "Unknown":
            return
            
        # Lưu thông tin về lần match này
        self.last_match_frame = current_frame
        
        # Nếu đang nhận diện identity mới - Chuyển chuỗi thành FaceIdentity nếu cần
        if isinstance(identity, str):
            # Tạo một FaceIdentity từ chuỗi
            try:
                # Import động để tránh import circular
                import importlib
                face_identity_module = importlib.import_module("src.face_recognition.face_database")
                constants_module = importlib.import_module("src.constants")
                
                # Lấy các class cần thiết
                FaceIdentity = getattr(face_identity_module, "FaceIdentity")
                IdentityType = getattr(constants_module, "IdentityType")
                
                # Lưu tên gốc trước khi chuyển đổi
                identity_name = identity
                identity_id = identity_name.lower().replace(" ", "_")
                
                # Tạo FaceIdentity object
                identity = FaceIdentity(
                    name=identity_name,
                    id=identity_id,
                    type=IdentityType.UNKNOWN
                )
                logger.info(f"Đã chuyển đổi chuỗi '{identity_name}' thành đối tượng FaceIdentity với id='{identity_id}'")
            except Exception as e:
                logger.error(f"Lỗi khi chuyển đổi chuỗi thành FaceIdentity: {str(e)}")
                return
        
        # Lưu kết quả nhận diện
        match = IdentityMatch(
            identity=identity, 
            similarity=similarity,
            frame_number=current_frame
        )
        self.identity_matches.append(match)
        self.face_detected_frames += 1
        
        # Cập nhật điểm cho danh tính này
        identity_id = identity.id
        
        # Cập nhật điểm cho danh tính này
        if identity_id not in self._identity_scores:
            self._identity_scores[identity_id] = 0
        
        # Tính điểm mới dựa trên độ tương đồng - Tăng điểm nhanh hơn
        if similarity >= 0.7:  # Rất giống - hạ ngưỡng và tăng điểm
            score_increment = 35.0
        elif similarity >= 0.5:  # Khá giống - hạ ngưỡng và tăng điểm
            score_increment = 25.0
        elif similarity >= 0.35:  # Hơi giống - hạ ngưỡng và tăng điểm
            score_increment = 15.0
        else:  # Không quá giống
            score_increment = 5.0
            
        self._identity_scores[identity_id] += score_increment
        
        # Giới hạn tối đa là 100
        self._identity_scores[identity_id] = min(self._identity_scores[identity_id], 100.0)
        
        # In thông tin về điểm
        logger.info(f"Identity '{identity.name}' (id={identity_id}) có điểm = {self._identity_scores[identity_id]:.2f}")
        
        # Cập nhật danh tính hiện tại
        changed = self._update_current_identity()
        
        # In thông tin về danh tính hiện tại
        if changed and self.current_identity is not None:
            logger.info(f"Đã cập nhật danh tính track_id={self.track_id} thành: {self.current_identity.name} (score={self.confidence_score:.2f})")
        return

    def _update_current_identity(self) -> bool:
        """Cập nhật danh tính hiện tại dựa trên lịch sử nhận diện.

        Returns:
            bool: True nếu danh tính được thay đổi, False nếu không
        """
        if not self._identity_scores:
            return False
            
        # Tìm danh tính có điểm cao nhất
        best_identity_id = max(self._identity_scores, key=self._identity_scores.get)
        best_score = self._identity_scores[best_identity_id]
        
        # Tìm danh tính tương ứng trong lịch sử nhận diện
        best_identity = None
        for match in reversed(self.identity_matches):
            if match.identity.id == best_identity_id:
                best_identity = match.identity
                break
                
        if best_identity is None:
            return False
            
        identity_changed = False
        
        # Cập nhật danh tính nếu:
        # 1. Chưa có danh tính hiện tại
        # 2. Danh tính mới khác danh tính hiện tại VÀ có điểm cao hơn ngưỡng
        # 3. Danh tính hiện tại giống danh tính mới (cập nhật điểm tin cậy)
        if self.current_identity is None:
            self.current_identity = best_identity
            identity_changed = True
        elif self.current_identity.id != best_identity.id and best_score >= 40:
            # Chỉ chuyển danh tính khi điểm đủ cao
            self.current_identity = best_identity
            identity_changed = True
        
        # Cập nhật điểm và mức độ tin cậy
        self.confidence_score = best_score
        self._update_confidence_level()
        
        return identity_changed
        
    def _update_confidence_level(self) -> None:
        """Cập nhật mức độ tin cậy dựa trên điểm."""
        if self.confidence_score >= 80:
            self.confidence_level = IdentityConfidenceLevel.VERY_HIGH
        elif self.confidence_score >= 60:
            self.confidence_level = IdentityConfidenceLevel.HIGH
        elif self.confidence_score >= 40:
            self.confidence_level = IdentityConfidenceLevel.MEDIUM
        elif self.confidence_score >= 20:
            self.confidence_level = IdentityConfidenceLevel.LOW
        else:
            self.confidence_level = IdentityConfidenceLevel.UNKNOWN
            
    def _decay_confidence(self) -> None:
        """Giảm điểm tin cậy khi không có nhận diện mới."""
        # Nếu không có danh tính, không cần làm gì
        if self.current_identity is None:
            return
            
        # Lấy điểm hiện tại của danh tính
        identity_id = self.current_identity.id
        if identity_id in self._identity_scores:
            # Giảm điểm 5% mỗi lần
            self._identity_scores[identity_id] *= 0.95
            
            # Cập nhật lại điểm confidence score và mức độ tin cậy
            self.confidence_score = self._identity_scores[identity_id]
            self._update_confidence_level()
            
            # Nếu điểm quá thấp, reset danh tính
            if self.confidence_score < 10:
                self.current_identity = None
                self.confidence_level = IdentityConfidenceLevel.UNKNOWN
        
    def get_identity_info(self) -> Tuple[Optional[FaceIdentity], float, IdentityConfidenceLevel]:
        """Lấy thông tin danh tính hiện tại.

        Returns:
            Tuple[Optional[FaceIdentity], float, IdentityConfidenceLevel]: 
            Danh tính, điểm tin cậy, mức độ tin cậy
        """
        return self.current_identity, self.confidence_score, self.confidence_level
        
    def get_identity_name(self) -> str:
        """Lấy tên hiển thị của danh tính.

        Returns:
            str: Tên hiển thị kèm loại (nhân viên, khách hàng, v.v.)
        """
        if self.current_identity is None:
            return "Unknown"
            
        name = self.current_identity.name
        
        if self.current_identity.type == IdentityType.EMPLOYEE:
            prefix = "📛"  # Nhân viên
        elif self.current_identity.type == IdentityType.KNOWN_CUSTOMER:
            prefix = "🌟"  # Khách hàng đã biết
        else:
            prefix = "👤"  # Người lạ
            
        # Thêm thông tin về mức độ tin cậy
        if self.confidence_level == IdentityConfidenceLevel.VERY_HIGH:
            suffix = ""  # Rất tin cậy, không cần đánh dấu
        elif self.confidence_level == IdentityConfidenceLevel.HIGH:
            suffix = "✓"  # Tin cậy cao
        elif self.confidence_level == IdentityConfidenceLevel.MEDIUM:
            suffix = "?"  # Tin cậy trung bình
        elif self.confidence_level == IdentityConfidenceLevel.LOW:
            suffix = "??"  # Tin cậy thấp
        else:
            suffix = "???"  # Không xác định
            
        return f"{prefix} {name} {suffix}"


class IdentityTracker:
    """Quản lý danh tính cho nhiều đối tượng theo dõi.

    Lớp này theo dõi danh tính của tất cả đối tượng đang xuất hiện,
    quản lý việc cập nhật danh tính và xử lý các tình huống phức tạp.

    Attributes:
        tracked_persons: Từ điển các đối tượng đang theo dõi, key là track_id
        frame_counter: Số lượng frame đã xử lý
        face_detector: Đối tượng phát hiện khuôn mặt
        face_recognizer: Đối tượng nhận diện khuôn mặt
        face_detection_interval: Khoảng cách giữa các lần phát hiện khuôn mặt
        min_face_similarity: Ngưỡng tối thiểu để coi là nhận diện hợp lệ
        debug: Chế độ debug
    """
    
    def __init__(
        self,
        face_detector=None,
        face_recognizer=None,
        face_detection_interval: int = 5,
        min_face_similarity: float = 0.35,
        debug: bool = False
    ):
        """Khởi tạo identity tracker.
        
        Args:
            face_detector: Đối tượng phát hiện khuôn mặt
            face_recognizer: Đối tượng nhận diện khuôn mặt
            face_detection_interval: Khoảng cách giữa các lần phát hiện khuôn mặt
            min_face_similarity: Ngưỡng tối thiểu để coi là nhận diện hợp lệ
            debug: Chế độ debug
        """
        self.tracked_persons: Dict[int, TrackedPerson] = {}
        self.frame_counter = 0
        self.face_detector = face_detector
        self.face_recognizer = face_recognizer
        self.face_detection_interval = face_detection_interval
        self.min_face_similarity = min_face_similarity
        self.debug = debug
        
    def update(self, track_ids: List[int], frame_number: int) -> None:
        """Cập nhật danh sách các đối tượng đang theo dõi.

        Args:
            track_ids: Danh sách ID của các đối tượng đang theo dõi
            frame_number: Số thứ tự frame hiện tại
        """
        self.frame_counter = frame_number
        
        # Cập nhật các đối tượng hiện có
        for track_id in track_ids:
            if track_id not in self.tracked_persons:
                self.tracked_persons[track_id] = TrackedPerson(track_id)
            self.tracked_persons[track_id].update(has_face_match=False, 
                                                 current_frame=frame_number)
            
        # Xóa các đối tượng không còn xuất hiện sau một thời gian
        # (Giữ lại trong một khoảng thời gian để tránh tạo mới quá nhiều)
        ids_to_remove = []
        for track_id, person in self.tracked_persons.items():
            if track_id not in track_ids and frame_number - person.last_match_frame > 120:
                ids_to_remove.append(track_id)
                
        for track_id in ids_to_remove:
            del self.tracked_persons[track_id]
            
    def add_face_recognition(
        self, 
        track_id: int, 
        identity: FaceIdentity, 
        similarity: float
    ) -> None:
        """Thêm kết quả nhận diện khuôn mặt cho một đối tượng.

        Args:
            track_id: ID của đối tượng
            identity: Danh tính nhận diện được
            similarity: Độ tương đồng (0-1)
        """
        if track_id not in self.tracked_persons:
            self.tracked_persons[track_id] = TrackedPerson(track_id)
            
        person = self.tracked_persons[track_id]
        person.add_identity_match(identity, similarity, self.frame_counter)
        
    def get_person_identity(self, track_id: int) -> Tuple[Optional[FaceIdentity], float, IdentityConfidenceLevel]:
        """Lấy thông tin danh tính của một đối tượng.

        Args:
            track_id: ID của đối tượng

        Returns:
            Tuple[Optional[FaceIdentity], float, IdentityConfidenceLevel]: 
            Danh tính, điểm tin cậy, mức độ tin cậy
        """
        if track_id not in self.tracked_persons:
            return None, 0.0, IdentityConfidenceLevel.UNKNOWN
            
        return self.tracked_persons[track_id].get_identity_info()
        
    def get_all_identities(self) -> Dict[int, Tuple[Optional[FaceIdentity], float, IdentityConfidenceLevel]]:
        """Lấy danh tính của tất cả đối tượng đang theo dõi.

        Returns:
            Dict[int, Tuple[Optional[FaceIdentity], float, IdentityConfidenceLevel]]: 
            Từ điển với key là track_id, value là (danh tính, điểm, mức độ tin cậy)
        """
        return {
            track_id: person.get_identity_info()
            for track_id, person in self.tracked_persons.items()
        } 

    def update_identities(self, tracks: List[Tuple], frame: np.ndarray):
        """Cập nhật danh tính cho đối tượng theo dõi.
        
        Args:
            tracks: Danh sách các tracks [(bbox, track_id, det_conf, class_id), ...]
            frame: Khung hình hiện tại
        """
        # Chỉ tăng frame counter một lần ở đầu hàm
        self.frame_counter += 1
        
        # Ghi lại số lượng tracks
        logger.info(f"Đang cập nhật danh tính cho {len(tracks)} tracks (frame #{self.frame_counter})")
        logger.info(f"DEBUG: face_detection_interval={self.face_detection_interval}, frame_counter={self.frame_counter}")
        
        # Cập nhật TrackedPerson cho mỗi track
        for track in tracks:
            bbox, track_id, det_conf, class_id = track
            
            # Chỉ xử lý người (class_id = 0)
            if class_id != 0:  
                continue
                
            # Nếu track_id chưa tồn tại, tạo mới
            if track_id not in self.tracked_persons:
                self.tracked_persons[track_id] = TrackedPerson(track_id)
                
            # Lấy đối tượng TrackedPerson
            person = self.tracked_persons[track_id]
            
            # Chỉ thực hiện phát hiện khuôn mặt theo định kỳ
            should_detect = (self.frame_counter % self.face_detection_interval == 0)
            
            # Thêm điều kiện: luôn phát hiện khuôn mặt cho người chưa có danh tính
            identity_info = person.get_identity_info()
            if identity_info[0] == "Unknown" or identity_info[2] == IdentityConfidenceLevel.UNKNOWN:
                should_detect = True
                logger.info(f"Track {track_id}: Bắt buộc phát hiện khuôn mặt vì chưa có danh tính hoặc độ tin cậy thấp")
            
            logger.info(f"Track {track_id}: Nên phát hiện khuôn mặt? {should_detect}")
            
            if should_detect:
                logger.info(f"Track {track_id}: Bắt đầu phát hiện khuôn mặt (frame #{self.frame_counter})")
                # Tách bounding box
                x1, y1, x2, y2 = bbox
                
                try:
                    # Chuyển đổi tọa độ thành số nguyên để tránh lỗi khi cắt ảnh
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Mở rộng bbox để phát hiện khuôn mặt tốt hơn
                    h = y2 - y1
                    padding = int(0.1 * h)  # 10% padding
                    face_y1 = int(max(0, y1 - padding))
                    face_y2 = int(min(frame.shape[0], y1 + int(0.7 * h)))  # 70% chiều cao (phần trên của người)
                    face_x1 = int(max(0, x1 - padding))
                    face_x2 = int(min(frame.shape[1], x2 + padding))
                    
                    # Cắt vùng khuôn mặt để phát hiện
                    face_region = frame[face_y1:face_y2, face_x1:face_x2]
                    
                    # Kiểm tra kích thước face_region
                    logger.debug(f"Track {track_id}: face_region shape = {face_region.shape if face_region is not None else 'None'}")
                    
                    # Phát hiện khuôn mặt trong vùng đã cắt
                    if self.face_detector is not None and face_region.size > 0:
                        # Thay thế detect_face bằng detect()
                        face_locations = self.face_detector.detect(face_region)
                        logger.info(f"Track {track_id}: Phát hiện {len(face_locations)} khuôn mặt")
                        
                        # Nếu phát hiện được ít nhất một khuôn mặt
                        if face_locations and len(face_locations) > 0:
                            # Lấy khuôn mặt lớn nhất
                            largest_face = max(face_locations, 
                                             key=lambda loc: (loc[2] - loc[0]) * (loc[1] - loc[3]))
                            
                            logger.debug(f"Track {track_id}: largest_face = {largest_face}")
                            
                            # Trích xuất khuôn mặt từ vùng
                            face_img = self.face_detector.extract_face(face_region, largest_face)
                            face_confidence = 1.0  # Giả định độ tin cậy là 100%
                            
                            # Kiểm tra khuôn mặt đã trích xuất
                            if face_img is not None:
                                logger.debug(f"Track {track_id}: extracted face shape = {face_img.shape if face_img is not None else 'None'}")
                            
                            # Nhận diện khuôn mặt
                            if self.face_recognizer is not None and face_img is not None and face_img.size > 0:
                                # Lấy danh sách danh tính đã biết
                                known_identities = self.face_recognizer.get_known_identities()
                                logger.debug(f"Danh sách danh tính đã biết: {[(identity['id'], identity['name']) for identity in known_identities]}")
                                
                                # Nhận diện khuôn mặt
                                identity, similarity = self.face_recognizer.recognize(face_img)
                                logger.info(f"Track {track_id}: face recognition result: identity={identity}, similarity={similarity:.4f}")
                                
                                # Nếu similarity vượt qua ngưỡng, cập nhật danh tính
                                if identity != "Unknown" and similarity > self.min_face_similarity:
                                    person.add_identity_match(identity, similarity, self.frame_counter)
                                    logger.info(f"Track {track_id}: đã thêm match - identity={identity}, similarity={similarity:.4f}")
                                    
                                    # Lấy thông tin danh tính sau khi cập nhật
                                    identity_info = person.get_identity_info()
                                    logger.info(f"Track {track_id}: Sau khi cập nhật - identity={identity_info[0]}, score={identity_info[1]:.2f}, confidence={identity_info[2]}")
                                else:
                                    logger.info(f"Track {track_id}: không match - identity={identity}, similarity={similarity:.4f} (ngưỡng: {self.min_face_similarity})")
                            else:
                                logger.warning(f"Track {track_id}: khuôn mặt trích xuất không hợp lệ hoặc recognizer là None")
                        else:
                            logger.debug(f"Không phát hiện được khuôn mặt cho track_id {track_id}")
                    else:
                        logger.warning(f"Track {track_id}: face_detector là None hoặc face_region không hợp lệ")
                except Exception as e:
                    logger.warning(f"Lỗi khi xử lý khuôn mặt cho track_id {track_id}: {str(e)}")
                    
            # Giảm dần độ tin cậy của danh tính
            person._decay_confidence()
            
        # Xóa các tracked_persons không còn tồn tại trong tracks hiện tại
        current_track_ids = [track[1] for track in tracks if track[3] == 0]  # Chỉ lấy track_id của người
        track_ids_to_remove = [tid for tid in self.tracked_persons if tid not in current_track_ids]
        
        for track_id in track_ids_to_remove:
            del self.tracked_persons[track_id]

        # Vẽ khung người nếu ở chế độ debug
        if self.debug:
            for track in tracks:
                bbox, track_id, confidence_score, class_id = track
                if class_id != 0:  # Chỉ vẽ người
                    continue
                    
                x, y, x2, y2 = bbox
                # Chuyển đổi tọa độ thành số nguyên cho việc vẽ
                x, y, x2, y2 = int(x), int(y), int(x2), int(y2)
                
                identity, identity_score, _ = self.get_person_identity(track_id)
                
                # Màu sắc dựa trên danh tính
                if identity == "Unknown":
                    color = (0, 0, 255)  # Đỏ cho người lạ
                else:
                    color = (0, 255, 0)  # Xanh lá cho người đã biết
                
                # Vẽ khung và thông tin
                cv2.rectangle(frame, (x, y), (x2, y2), color, 2)
                
                # Hiển thị thông tin
                info_text = f"ID: {track_id} - {identity}"
                if identity != "Unknown":
                    info_text += f" ({identity_score:.2f})"
                
                cv2.putText(frame, info_text, (x, y - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Gỡ bỏ những tracked_person không còn xuất hiện nhiều frame
        self._remove_old_tracked_persons()
    
    def _remove_old_tracked_persons(self, max_frames_disappeared: int = 120) -> None:
        """Xóa các đối tượng theo dõi đã không xuất hiện quá lâu.
        
        Args:
            max_frames_disappeared: Số frame tối đa một đối tượng có thể vắng mặt
                trước khi bị xóa khỏi danh sách theo dõi
        """
        ids_to_remove = []
        for track_id, person in self.tracked_persons.items():
            frames_disappeared = self.frame_counter - person.last_match_frame
            if frames_disappeared > max_frames_disappeared:
                ids_to_remove.append(track_id)
                
        for track_id in ids_to_remove:
            del self.tracked_persons[track_id] 