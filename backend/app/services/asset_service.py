from pathlib import Path
from uuid import UUID
from typing import Optional
import aiofiles
import shutil
from app.config.storage import ASSETS_DIR, get_asset_dir as get_asset_dir_from_storage
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class AssetService:
    @staticmethod
    def get_asset_dir(doc_id: UUID) -> Path:
        """Get asset directory for a document."""
        return get_asset_dir_from_storage(str(doc_id))

    @staticmethod
    def get_shared_asset_dir() -> Path:
        """Get shared asset directory."""
        return get_asset_dir_from_storage()  # None returns shared directory

    @staticmethod
    async def save_asset(
        doc_id: UUID,
        filename: str,
        content: bytes,
        is_shared: bool = False
    ) -> Path:
        """Save an asset file."""
        if is_shared:
            asset_dir = AssetService.get_shared_asset_dir()
        else:
            asset_dir = AssetService.get_asset_dir(doc_id)
        
        asset_dir.mkdir(parents=True, exist_ok=True)
        asset_path = asset_dir / filename
        
        async with aiofiles.open(asset_path, 'wb') as f:
            await f.write(content)
        
        logger.info(f"Saved asset: {asset_path}")
        return asset_path

    @staticmethod
    async def copy_asset(
        source_path: Path,
        doc_id: UUID,
        filename: Optional[str] = None,
        is_shared: bool = False
    ) -> Path:
        """Copy an asset file."""
        if is_shared:
            asset_dir = AssetService.get_shared_asset_dir()
        else:
            asset_dir = AssetService.get_asset_dir(doc_id)
        
        asset_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            filename = source_path.name
        
        dest_path = asset_dir / filename
        
        # Use shutil for copying
        shutil.copy2(source_path, dest_path)
        
        logger.info(f"Copied asset: {source_path} -> {dest_path}")
        return dest_path

    @staticmethod
    def get_asset_url(doc_id: UUID, filename: str, is_shared: bool = False) -> str:
        """Generate URL for an asset."""
        if is_shared:
            return f"/api/assets/shared/{filename}"
        return f"/api/assets/{doc_id}/{filename}"

    @staticmethod
    async def delete_asset(doc_id: UUID, filename: str) -> bool:
        """Delete an asset file."""
        asset_path = AssetService.get_asset_dir(doc_id) / filename
        if asset_path.exists():
            asset_path.unlink()
            logger.info(f"Deleted asset: {asset_path}")
            return True
        return False

    @staticmethod
    async def list_assets(doc_id: UUID) -> list[Path]:
        """List all assets for a document."""
        asset_dir = AssetService.get_asset_dir(doc_id)
        if not asset_dir.exists():
            return []
        return list(asset_dir.iterdir())

    @staticmethod
    async def cleanup_unused_assets() -> int:
        """Clean up unused assets (future implementation)."""
        # TODO: Implement cleanup logic
        return 0

