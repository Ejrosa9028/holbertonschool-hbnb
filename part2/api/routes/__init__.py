from .user_routes import user_ns
from .place_routes import place_ns
from .review_routes import review_ns

# Exponer estos namespaces para importarlos desde api.app
__all__ = ["user_ns", "place_ns", "review_ns"]
