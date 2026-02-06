# Streamify Common

Shared Python library for Streamify microservices.

## Installation

```bash
pip install -e .
```

## Usage

```python
from streamify_common.auth.jwt import generate_token, verify_token
from streamify_common.exceptions import NotFoundError
from streamify_common.models.base import BaseModel
```

## Components

- **auth**: JWT authentication utilities
- **models**: Base models and mixins
- **serializers**: Base serializers
- **exceptions**: Custom exceptions
- **middleware**: Common middleware
- **constants**: Error codes and messages
- **utils**: Utility functions
