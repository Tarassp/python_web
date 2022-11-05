from enum import Enum

class FileExtension(Enum):
    TXT = 'txt'
    DOC = 'doc'
    DOCX = 'docx'
    PDF = 'pdf'
    XLSX = 'xlsx'
    PPTX = 'pptx'
    
    JPEG = 'jpeg'
    JPG = 'jpg'
    PNG = 'png'
    SVG = 'svg'
    
    AVI = 'avi'
    MP4 = 'mp4'
    MOV = 'mov'
    MKV = 'mkv'
    
    MP3 = 'mp3'
    OGG = 'ogg'
    WAV = 'wav'
    AMR = 'amr'
    
    ZIP = 'zip'
    GZ = 'gz'
    TAR = 'tar'
    
    UNKNOWN = 'unknown'
    
    @property
    def is_unknown(self):
        return self == FileExtension.UNKNOWN
        
    @classmethod
    def _missing_(cls, value: str):
        for item in cls.__members__.values():
            if isinstance(value, str) and item.value == value.lower():
                return item
        else:
            return cls.UNKNOWN

class FileCategory(Enum):
    DOCUMENTS = [FileExtension.TXT, FileExtension.DOC, FileExtension.DOCX, FileExtension.PDF, FileExtension.XLSX, FileExtension.PPTX]
    IMAGES = [FileExtension.JPEG, FileExtension.JPG, FileExtension.PNG, FileExtension.SVG]
    AUDIO = [FileExtension.MP3, FileExtension.OGG, FileExtension.WAV, FileExtension.AMR]
    VIDEO = [FileExtension.AVI, FileExtension.MP4, FileExtension.MOV, FileExtension.MKV]
    ARCHIVES = [FileExtension.ZIP, FileExtension.GZ, FileExtension.TAR]
    UNKNOWNS = FileExtension.UNKNOWN
    
    @classmethod
    def _missing_(cls, value):
        for item in cls.__members__.values():
            if value in item.value:
                return item
        return cls.UNKNOWNS
    
    @property
    def folder_name(self):
        return self.name.lower()
    
    @property
    def is_unknowns(self):
        return self == FileCategory.UNKNOWNS
    
    @classmethod
    @property
    def reserved_folders(cls):
        return [x.lower() for x in cls._member_names_]
