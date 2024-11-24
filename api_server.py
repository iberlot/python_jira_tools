from fastapi import FastAPI, Query, HTTPException, Path, Body
from typing import Optional
from jira_data_library.manager import JiraManager

app = FastAPI()

# Inicializa tu manager (puedes pasar configuraciones aquí)
jira_manager = JiraManager(base_url="https://web",
                           username="email@gmail.com",
                           token="token")

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Obtén detalles de una tarea"""
    return jira_manager.get_task(task_id)

@app.get("/sprints/{sprint_id}")
async def get_sprint(sprint_id: str):
    """Obtén detalles de un sprint"""
    return jira_manager.get_sprint(sprint_id)

@app.get("/list_projects")
async def get_list_projects():
    """Obtén detalles de un sprint"""
    return jira_manager.get_list_projects()

@app.get("/get_project/{project_key}")
async def get_project(project_key):
    """Obtén detalles de un sprint"""
    return jira_manager.get_project(project_key)

## Board APIs

@app.get("/get_board/{board_key}")
async def get_board(board_key):
    return jira_manager.get_board(board_key)

@app.get("/get_project_boards/{project_key}")
async def get_project_boards(project_key):
    return jira_manager.get_project_boards(project_key)

@app.get("/get_board_sprints/{project_key}")
async def get_project_sprints(project_key):
    """Obtén detalles de un sprint"""
    return jira_manager.get_board_sprints(project_key)

@app.get("/get_sprint/{sprint_key}")
async def get_sprint(sprint_key):
    """Obtén detalles de un sprint"""
    return jira_manager.get_sprint(sprint_key)

## Tasks APIs


@app.get("/project/{project_key}/issues")
async def get_project_issues(
    project_key: str,
    issue_type: Optional[str] = Query(None, description="Filtrar por tipo de issue"),
    assignee: Optional[str] = Query(None, description="Filtrar por usuario asignado"),
):
    """
    Obtiene las issues de un proyecto, con filtros opcionales por tipo de issue y usuario asignado.

    Args:
        project_key (str): Clave del proyecto.
        issue_type (str, optional): Tipo de issue (por ejemplo, "Bug", "Task").
        assignee (str, optional): Usuario asignado.

    Returns:
        list: Lista de issues.
    """
    return jira_manager.get_project_issues(project_key, issue_type, assignee)


@app.get("/sprint/{sprint_id}/issues")
async def get_sprint_issues(
    sprint_id: int,
    issue_type: Optional[str] = Query(None, description="Filtrar por tipo de issue"),
    assignee: Optional[str] = Query(None, description="Filtrar por usuario asignado"),
):
    """
    Obtiene las issues de un sprint, con filtros opcionales por tipo de issue y usuario asignado.

    Args:
        sprint_id (int): ID del sprint.
        issue_type (str, optional): Tipo de issue (por ejemplo, "Bug", "Task").
        assignee (str, optional): Usuario asignado.

    Returns:
        list: Lista de issues.
    """
    return jira_manager.get_sprint_issues(sprint_id, issue_type, assignee)


@app.get("/tasks/{issue_id}/comments", tags=["Comments"])
async def get_task_comments(issue_id: str = Path(..., description="ID o clave de la tarea")):
    """
    Obtiene los comentarios de una tarea.
    """
    try:
        comments = jira_manager.get_task_comments(issue_id)
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks/{issue_id}/comments", tags=["Comments"])
async def add_task_comment(
    issue_id: str = Path(..., description="ID o clave de la tarea"),
    comment_body: str = Body(..., description="Cuerpo del comentario")
):
    """
    Agrega un comentario a una tarea.
    """
    try:
        comment = jira_manager.add_task_comment(issue_id, comment_body)
        return {"comment": comment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{issue_id}/comments/{comment_id}", tags=["Comments"])
async def update_task_comment(
    issue_id: str = Path(..., description="ID o clave de la tarea"),
    comment_id: str = Path(..., description="ID del comentario"),
    new_body: str = Body(..., description="Nuevo contenido del comentario")
):
    """
    Actualiza un comentario de una tarea.
    """
    try:
        updated_comment = jira_manager.update_task_comment(issue_id, comment_id, new_body)
        return {"updated_comment": updated_comment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{issue_id}/comments/{comment_id}", tags=["Comments"])
async def delete_task_comment(
    issue_id: str = Path(..., description="ID o clave de la tarea"),
    comment_id: str = Path(..., description="ID del comentario")
):
    """
    Elimina un comentario de una tarea.
    """
    try:
        success = jira_manager.delete_task_comment(issue_id, comment_id)
        if success:
            return {"message": "Comentario eliminado exitosamente"}
        else:
            raise HTTPException(status_code=404, detail="No se pudo eliminar el comentario")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_attachments/{task_key}")
async def get_attachments(task_key: str):
    """
    Obtén los adjuntos de una tarea.

    Args:
        task_key (str): Clave de la tarea.

    Returns:
        dict: Diccionario con la clave de la tarea y los adjuntos descargados.
    """
    try:
        # Llama al método del AttachmentManager
        attachments = jira_manager.get_task_attachments(task_key)
        return attachments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
