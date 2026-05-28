import React, { useState, useEffect } from 'react';
import { getProjects, createProject, updateProject, deleteProject, getUsers } from '../services/api';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import './Projects.css';

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [users, setUsers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    status: 'planning',
    start_date: '',
    end_date: '',
    assigned_to: []
  });
  const { user } = useAuth();

  const userRole = user?.role?.toLowerCase();
  const canEdit = userRole === 'admin' || userRole === 'manager';

  useEffect(() => {
    loadProjects();
    if (canEdit) {
      loadUsers();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);  

  const loadProjects = async () => {
    try {
      const response = await getProjects();
      setProjects(response.data);
    } catch (error) {
      toast.error('Failed to load projects');
    }
  };

  const loadUsers = async () => {
    try {
      const response = await getUsers();
      setUsers(response.data);
    } catch (error) {
      console.error('Failed to load users');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name) {
      toast.error('Project name is required');
      return;
    }
    if (!formData.start_date) {
      toast.error('Start date is required');
      return;
    }
    
    try {
      const submitData = {
        name: formData.name,
        description: formData.description,
        status: formData.status,
        start_date: formData.start_date,
        end_date: formData.end_date || null,
        assigned_to: formData.assigned_to || []
      };
      
      console.log('Submitting project:', submitData);
      
      if (editingProject) {
        await updateProject(editingProject.id, submitData);
        toast.success('Project updated successfully');
      } else {
        await createProject(submitData);
        toast.success('Project created successfully');
      }
      setShowForm(false);
      setEditingProject(null);
      setFormData({ 
        name: '', 
        description: '', 
        status: 'planning', 
        start_date: '', 
        end_date: '',
        assigned_to: []
      });
      loadProjects();
    } catch (error) {
      console.error('Error details:', error.response?.data);
      if (error.response?.data) {
        const errors = error.response.data;
        if (typeof errors === 'object') {
          const errorMessages = Object.values(errors).flat().join(', ');
          toast.error(errorMessages);
        } else {
          toast.error('Failed to save project');
        }
      } else {
        toast.error('Failed to save project');
      }
    }
  };

  const handleEdit = (project) => {
    setEditingProject(project);
    setFormData({
      name: project.name,
      description: project.description,
      status: project.status,
      start_date: project.start_date,
      end_date: project.end_date || '',
      assigned_to: project.assigned_to || []
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await deleteProject(id);
        toast.success('Project deleted successfully');
        loadProjects();
      } catch (error) {
        toast.error('Failed to delete project');
      }
    }
  };

  const handleAssignedToChange = (userId) => {
    const currentAssigned = [...formData.assigned_to];
    if (currentAssigned.includes(userId)) {
      setFormData({
        ...formData,
        assigned_to: currentAssigned.filter(id => id !== userId)
      });
    } else {
      setFormData({
        ...formData,
        assigned_to: [...currentAssigned, userId]
      });
    }
  };

  return (
    <div className="projects-container">
      <div className="page-header">
        <h1>Projects</h1>
        <button className="btn-add" onClick={() => setShowForm(true)}>
          + Add Project
        </button>
      </div>

      {showForm && (
        <div className="modal">
          <div className="modal-content">
            <h2>{editingProject ? 'Edit Project' : 'Add New Project'}</h2>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Project Name *"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
              />
              <textarea
                placeholder="Description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                required
              />
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
              >
                <option value="planning">Planning</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
              </select>
              <label>Start Date *</label>
              <input
                type="date"
                value={formData.start_date}
                onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                required
              />
              <label>End Date (Optional)</label>
              <input
                type="date"
                value={formData.end_date}
                onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
              />
              
              <label>Assign Members (Optional)</label>
              <div className="assigned-members">
                {users.map(u => (
                  <label key={u.id} className="member-checkbox">
                    <input
                      type="checkbox"
                      checked={formData.assigned_to.includes(u.id)}
                      onChange={() => handleAssignedToChange(u.id)}
                    />
                    {u.username} ({u.role})
                  </label>
                ))}
              </div>
              
              <div className="modal-buttons">
                <button type="submit">Save</button>
                <button type="button" onClick={() => {
                  setShowForm(false);
                  setEditingProject(null);
                }}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="projects-list">
        {projects.map(project => (
          <div key={project.id} className="project-card">
            <div className="project-info">
              <h3>{project.name}</h3>
              <p>{project.description}</p>
              <div className="project-meta">
                <span className={`status ${project.status}`}>{project.status}</span>
                <span>Start: {project.start_date}</span>
                <span>End: {project.end_date || 'Not set'}</span>
              </div>
            </div>
            {canEdit && (
              <div className="project-actions">
                <button className="btn-edit" onClick={() => handleEdit(project)}>Edit</button>
                <button className="btn-delete" onClick={() => handleDelete(project.id)}>Delete</button>
              </div>
            )}
          </div>
        ))}
        {projects.length === 0 && <p className="no-data">No projects found</p>}
      </div>
    </div>
  );
};

export default Projects;
