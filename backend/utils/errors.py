from fastapi import HTTPException, status


def bad_request(msg: str):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)


def not_found(msg: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
