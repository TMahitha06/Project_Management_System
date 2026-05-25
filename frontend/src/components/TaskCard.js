import React from 'react';

function TaskCard({ task, showButtons, onEdit, onDelete, onStatusChange }) {
    return (
        <div className="task-card">
            <div className="task-header">
                <h3>{task.title}</h3>
                <div className="task-actions">
                    <select
                        value={task.status}
                        onChange={(e) => onStatusChange(task.id, e.target.value)}
                        className="status-select"
                    >
                        <option value="pending">Pending</option>
                        <option value="in_progress">In Progress</option>
                        <option value="completed">Completed</option>
                    </select>
                    {showButtons && (
                        <>
                            <button className="btn-edit" onClick={() => onEdit(task)}>
                                Edit
                            </button>
                            <button className="btn-delete" onClick={() => onDelete(task.id)}>   
                                Delete
                            </button>
                        </>
                    )}
                </div>
            </div>
            <p>{task.description}</p>
            <div className="task-details">
                <span className={`priority-${task.priority}`}>
                    Priority: {task.priority}
                </span>
                <span>Project: {task.project_name}</span>
                <span>Due: {task.due_date}</span>
                <span>Assigned to: {task.assigned_to_name}</span>
            </div>
        </div>
    );
}

export default TaskCard;