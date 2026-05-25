import React from 'react';

function ProjectCard({ project, showButtons, onEdit, onDelete }) {
    return (
        <div className="project-card">
            <div className="project-header">
                <h3>{project.name}</h3>
                {showButtons && (
                    <div className="project-actions">
                        <button className="btn-edit" onClick={() => onEdit(project)}>
                             Edit
                        </button>
                        <button className="btn-delete" onClick={() => onDelete(project.id)}>
                            Delete
                        </button>
                    </div>
                )}
            </div>
            <p>{project.description}</p>
            <div className="project-details">
                <span className={`status ${project.status}`}>{project.status}</span>
                <span>Start: {project.start_date}</span>
                {project.end_date && <span>End: {project.end_date}</span>}
            </div>
        </div>
    );
}

export default ProjectCard;