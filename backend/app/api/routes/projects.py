from fastapi import APIRouter, HTTPException, status

from app.schemas.workflow_schemas import ProjectCreate, ProjectUpdate
from app.services.workflow_service import WorkflowService

router = APIRouter()
service = WorkflowService()


@router.post('/api/projects', status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate):
    project = service.create_project(payload.idea, payload.audience, payload.industry, payload.problem)
    return project


@router.get('/api/projects')
def list_projects():
    return {'projects': service.list_projects()}


@router.get('/api/projects/{project_id}')
def get_project(project_id: str):
    try:
        return service.get_project(project_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found')


@router.put('/api/projects/{project_id}')
def update_project(project_id: str, payload: ProjectUpdate):
    try:
        return service.update_project(project_id, payload.model_dump(exclude_unset=True))
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found') from exc


@router.post('/api/projects/{project_id}/discover')
def discover(project_id: str):
    try:
        return service.run_stage(project_id, 'discover')
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found') from exc


@router.post('/api/projects/{project_id}/position')
def position(project_id: str):
    try:
        return service.run_stage(project_id, 'position')
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found') from exc


@router.post('/api/projects/{project_id}/define')
def define(project_id: str):
    try:
        return service.run_stage(project_id, 'define')
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found') from exc


@router.post('/api/projects/{project_id}/express')
def express(project_id: str):
    try:
        return service.run_stage(project_id, 'express')
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found') from exc


@router.post('/api/projects/{project_id}/challenge')
def challenge(project_id: str):
    try:
        return service.run_stage(project_id, 'challenge')
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found') from exc


@router.post('/api/projects/{project_id}/finalize')
def finalize(project_id: str):
    try:
        return service.run_stage(project_id, 'finalize')
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found') from exc


@router.post('/api/projects/{project_id}/launch')
def launch(project_id: str):
    try:
        return service.run_stage(project_id, 'launch')
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found') from exc


@router.get('/api/projects/{project_id}/export')
def export_project(project_id: str):
    try:
        return service.export_brand(project_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found') from exc
