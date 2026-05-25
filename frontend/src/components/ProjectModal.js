import React, { useState, useEffect } from 'react';

function ProjectModal({ isOpen, project, userRole, users, onClose, onSave }) {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        status: 'active',
        start_date: '',
        end_date: '',
        assigned_to: []
    });

    useEffect(() => {
        if (project) {
            setFormData(project);
        } else {
            setFormData({
                name: '',
                description: '',
                status: 'active',
                start_date: '',
                end_date: '',
                assigned_to: []
            });
        }
    }, [project]);

    if (!isOpen) return null;

    return (
        <div className="modal">
            <div className="modal-content">
                <h2>{project ? 'Edit Project' : ' Create New Project'}</h2>
                <form onSubmit={(e) => {
                    e.preventDefault();
                    onSave(formData);
                }}>
                    <input
                        type="text"
                        placeholder="Project Name"
                        value={formData.name}
                        onChange={(e) => setFormData({...formData, name: e.target.value})}
                        required
                    />
                    <textarea
                        placeholder="Description"
                        value={formData.description}
                        onChange={(e) => setFormData({...formData, description: e.target.value})}
                        required
                    />
                    <select
                        value={formData.status}
                        onChange={(e) => setFormData({...formData, status: e.target.value})}>
                        <option value="planning">Planning</option>
                        <option value="active">Active</option>
                        <option value="completed">Completed</option>
                    </select>
                    <input
                        type="date"
                        value={formData.start_date}
                        onChange={(e) => setFormData({...formData, start_date: e.target.value})}
                        required
                    />
                    <input
                        type="date"
                        value={formData.end_date}
                        onChange={(e) => setFormData({...formData, end_date: e.target.value})}
                    />
                    {userRole === 'admin' && (
                        <select
                            multiple
                            value={formData.assigned_to}
                            onChange={(e) => setFormData({
                                ...formData,
                                assigned_to: Array.from(e.target.selectedOptions, option => Number(option.value))
                            })}>
                            {users.map(user => (
                                <option key={user.id} value={user.id}>{user.username} ({user.role})</option>
                            ))}
                        </select>
                    )}
                    <div className="modal-actions">
                        <button type="submit">Save</button>
                        <button type="button" onClick={onClose}>Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default ProjectModal;