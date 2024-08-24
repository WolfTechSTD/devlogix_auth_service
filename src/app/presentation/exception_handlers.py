from litestar import Request, Response, status_codes


def bad_request_exception_handler(
        _: Request,
        exc: Exception
) -> Response:
    return Response(
        content={
            "status_code": status_codes.HTTP_400_BAD_REQUEST,
            "detail": str(exc)
        },
        status_code=status_codes.HTTP_400_BAD_REQUEST
    )


def forbidden_exception_handler(
        _: Request,
        exc: Exception
) -> Response:
    return Response(
        content={
            "status_code": status_codes.HTTP_403_FORBIDDEN,
            "detail": str(exc)
        },
        status_code=status_codes.HTTP_403_FORBIDDEN
    )


def not_found_exception_handler(
        _: Request,
        exc: Exception
) -> Response:
    return Response(
        content={
            "status_code": status_codes.HTTP_404_NOT_FOUND,
            "detail": str(exc)
        },
        status_code=status_codes.HTTP_404_NOT_FOUND
    )
