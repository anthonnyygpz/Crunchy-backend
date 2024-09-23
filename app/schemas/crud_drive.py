from pydantic import BaseModel
from typing import Optional


class FolderInfo(BaseModel):
    folder_name: str
    id_folder: Optional[str] = None


class FolderContent(BaseModel):
    id: str
    title: str
    # mimeType: str
    # modifiedDate: str


class FileInfo(BaseModel):
    file_name: str
    content: str
    id_folder: str
