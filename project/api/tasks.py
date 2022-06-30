from core.celery import app


@app.task
def read_client_org(filename):
    """
    """
    pass

@app.task
def read_bills(filename):
    """
    """
    pass
