import React, { useState, useEffect } from 'react';

function TaskModal({ isOpen, task, projects, users, onClose, onSave }) {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        project: '',
        assigned_to: '',
        priority: 'medium',
        status: 'pending',
        due_date: ''
    });

    useEffect(() => {
        if (task) {
            setFormData(task);
        } else {
            setFormData({
                title: '',
                description: '',
                project: '',
                assigned_to: '',
                priority: 'medium',
                status: 'pending',
                due_date: ''
            });
        }
    }, [task]);

    if (!isOpen) return null;

    return (
        <div className="modal">
            <div className="modal-content">
                <h2>{task ? ' Edit Task' : 'Create New Task'}</h2>
                <form onSubmit={(e) => {
                    e.preventDefault();
                    onSave(formData);
                }}>
                    <input
                        type="text"
                        placeholder="Task Title"
                        value={formData.title}
                        onChange={(e) => setFormData({...formData, title: e.target.value})}
                        required
                    />
                    <textarea
                        placeholder="Description"
                        value={formData.description}
                        onChange={(e) => setFormData({...formData, description: e.target.value})}
                        required
                    />
                    <select
                        value={formData.project}
                        onChange={(e) => setFormData({...formData, project: e.target.value})}
                        required>
                        <option value="">Select Project</option>
                        {projects.map(project => (
                            <option key={project.id} value={project.id}>{project.name}</option>
                        ))}
                    </select>
                    <select
                        value={formData.assigned_to}
                        onChange={(e) => setFormData({...formData, assigned_to: e.target.value})}
                        required>
                        <option value="">Assign To</option>
                        {users.map(user => (
                            <option key={user.id} value={user.id}>{user.username}</option>
                        ))}
                    </select>
                    <select
                        value={formData.priority}
                        onChange={(e) => setFormData({...formData, priority: e.target.value})}>
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                    </select>
                    <input
                        type="date"
                        value={formData.due_date}
                        onChange={(e) => setFormData({...formData, due_date: e.target.value})}
                        required
                    />
                    <div className="modal-actions">
                        <button type="submit">Save</button>
                        <button type="button" onClick={onClose}>Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default TaskModal;