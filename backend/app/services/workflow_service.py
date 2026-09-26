from __future__ import annotations

import json
from html import escape
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from app.core.ai_client import DemoAIClient
from app.core.config import PROJECTS_FILE


class WorkflowService:
    def __init__(self) -> None:
        self.ai = DemoAIClient()

    def _load_projects(self) -> Dict[str, Dict[str, Any]]:
        if not PROJECTS_FILE.exists():
            return {}
        try:
            with PROJECTS_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}

    def _save_projects(self, data: Dict[str, Dict[str, Any]]) -> None:
        temporary_file = PROJECTS_FILE.with_suffix(".tmp")
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        temporary_file.replace(PROJECTS_FILE)

    def create_project(self, idea: str, audience: str | None, industry: str | None, problem: str | None) -> Dict[str, Any]:
        project_id = str(uuid4())
        now = datetime.now(timezone.utc).isoformat()
        project = {
            "project_id": project_id,
            "idea": idea,
            "audience": audience,
            "industry": industry,
            "problem": problem,
            "workflow_stage": "discover",
            "discovery": {},
            "positioning": {},
            "brand_definition": {},
            "expression": {},
            "challenge": {},
            "final_brand_system": {},
            "launch": {},
            "created_at": now,
            "updated_at": now,
        }
        projects = self._load_projects()
        projects[project_id] = project
        self._save_projects(projects)
        return project

    def get_project(self, project_id: str) -> Dict[str, Any]:
        project = self._load_projects().get(project_id)
        if not project:
            raise KeyError("Project not found")
        return project

    def list_projects(self) -> List[Dict[str, Any]]:
        projects = list(self._load_projects().values())
        return sorted(projects, key=lambda project: project.get("updated_at", ""), reverse=True)

    def update_project(self, project_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        projects = self._load_projects()
        if project_id not in projects:
            raise KeyError("Project not found")
        project = projects[project_id]
        project.update(payload)
        project["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save_projects(projects)
        return project

    def run_stage(self, project_id: str, stage: str) -> Dict[str, Any]:
        project = self.get_project(project_id)
        if stage == "discover":
            data = self.ai.generate_discovery(project["idea"], project.get("audience"), project.get("industry"), project.get("problem"))
            project["discovery"] = data
            project["workflow_stage"] = "position"
        elif stage == "position":
            data = self.ai.generate_positioning(project)
            project["positioning"] = data
            project["workflow_stage"] = "define"
        elif stage == "define":
            data = self.ai.generate_brand_definition(project)
            project["brand_definition"] = data
            project["workflow_stage"] = "express"
        elif stage == "express":
            data = self.ai.generate_expression(project)
            project["expression"] = data
            project["workflow_stage"] = "challenge"
        elif stage == "challenge":
            data = self.ai.generate_challenge(project)
            project["challenge"] = data
            project["workflow_stage"] = "finalize"
        elif stage == "finalize":
            data = self.ai.generate_final_brand_system(project)
            project["final_brand_system"] = data
            project["workflow_stage"] = "launch"
        elif stage == "launch":
            data = self.ai.generate_launch_plan(project)
            project["launch"] = data
            project["workflow_stage"] = "complete"
        else:
            raise ValueError("Unsupported workflow stage")

        project["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save_projects(self._load_projects() | {project_id: project})
        return {"project_id": project_id, "stage": stage, "data": data, "workflow_stage": project["workflow_stage"]}

    def export_brand(self, project_id: str) -> Dict[str, Any]:
        project = self.get_project(project_id)
        final = project.get("final_brand_system") or {}
        launch = project.get("launch") or {}
        if not final:
            raise ValueError("Brand system has not been finalized yet")

        html = f"""
        <html>
          <head><meta charset="utf-8"><title>{escape(str(final.get('brand_name', 'Brand')))}</title></head>
          <body>
            <h1>{escape(str(final.get('brand_name', 'Brand')))}</h1>
            <p><strong>Tagline:</strong> {escape(str(final.get('tagline', '')))}</p>
            <h2>Problem</h2>
            <p>{escape(str(final.get('problem', '')))}</p>
            <h2>Target Audience</h2>
            <p>{escape(str(final.get('target_audience', '')))}</p>
            <h2>Positioning</h2>
            <p>{escape(str(final.get('positioning', '')))}</p>
            <h2>Brand Personality</h2>
            <ul>{''.join(f'<li>{escape(str(item))}</li>' for item in final.get('brand_personality', []))}</ul>
            <h2>Launch Plan</h2>
            <p>{escape(str(launch.get('launch_summary', '')))}</p>
            <ul>{''.join(f'<li>{escape(str(item))}</li>' for item in launch.get('launch_checklist', []))}</ul>
          </body>
        </html>
        """

        personality_lines = '\n'.join(f'- {item}' for item in final.get('brand_personality', []))
        markdown = f"""# {final.get('brand_name', 'Brand')}\n\n**Tagline:** {final.get('tagline', '')}\n\n## Problem\n{final.get('problem', '')}\n\n## Target Audience\n{final.get('target_audience', '')}\n\n## Positioning\n{final.get('positioning', '')}\n\n## Brand Personality\n{personality_lines}\n"""
        if launch:
            checklist_lines = '\n'.join(f'- {item}' for item in launch.get('launch_checklist', []))
            markdown += f"\n## Launch Plan\n{launch.get('launch_summary', '')}\n\n### Checklist\n{checklist_lines}\n"

        return {"project_id": project_id, "final_brand_system": final, "html_export": html, "markdown_export": markdown}
