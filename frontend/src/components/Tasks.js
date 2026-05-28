import React, { useState, useEffect } from 'react';
import { getTasks, createTask, updateTask, deleteTask, markTaskComplete, verifyTask, resubmitTask, getProjects, getUsers } from '../services/api';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import './Tasks.css';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [users, setUsers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    project: '',
    assigned_to: '',
    priority: 'medium',
    due_date: ''
  });
  const { user } = useAuth();

  useEffect(() => {
    loadData();
    loadUsers();
  }, []);

  const loadData = async () => {
    try {
      const tasksRes = await getTasks();
      const projectsRes = await getProjects();
      setTasks(tasksRes.data);
      setProjects(projectsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const loadUsers = async () => {
    try {
      const response = await getUsers();
      setUsers(response.data);
    } catch (error) {
      console.error('Error loading users:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title) {
      toast.error('Task title is required');
      return;
    }
    if (!formData.project) {
      toast.error('Please select a project');
      return;
    }
    if (!formData.assigned_to) {
      toast.error('Please assign this task to someone');
      return;
    }
    if (!formData.due_date) {
      toast.error('Due date is required');
      return;
    }
    
    try {
      const submitData = {
        title: formData.title,
        description: formData.description,
        project: formData.project,
        assigned_to: formData.assigned_to,
        priority: formData.priority,
        due_date: formData.due_date
      };
      
      console.log('Submitting task:', submitData);
      
      if (editingTask) {
        await updateTask(editingTask.id, submitData);
        toast.success('Task updated successfully');
      } else {
        await createTask(submitData);
        toast.success('Task created successfully');
      }
      setShowForm(false);
      setEditingTask(null);
      setFormData({
        title: '',
        description: '',
        project: '',
        assigned_to: '',
        priority: 'medium',
        due_date: ''
      });
      loadData();
    } catch (error) {
      console.error('Error details:', error.response?.data);
      if (error.response?.data) {
        const errors = error.response.data;
        if (typeof errors === 'object') {
          const errorMessages = Object.values(errors).flat().join(', ');
          toast.error(errorMessages);
        } else {
          toast.error('Failed to save task');
        }
      } else {
        toast.error('Failed to save task');
      }
    }
  };

  const handleEdit = (task) => {
    setEditingTask(task);
    setFormData({
      title: task.title,
      description: task.description,
      project: task.project,
      assigned_to: task.assigned_to,
      priority: task.priority,
      due_date: task.due_date
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(id);
        toast.success('Task deleted successfully');
        loadData();
      } catch (error) {
        toast.error('Failed to delete task');
      }
    }
  };

  const handleStatusUpdate = async (taskId, newStatus) => {
    try {
      if (newStatus === 'completed') {
        await markTaskComplete(taskId);
        toast.success('Task marked as completed! Waiting for manager verification.');
      } else {
        await updateTask(taskId, { status: newStatus });
        toast.success('Task status updated');
      }
      loadData();
    } catch (error) {
      toast.error('Failed to update status');
    }
  };

  const handleVerify = async (taskId, action) => {
    const feedback = action === 'reject' ? prompt('Enter feedback for the member:') : '';
    try {
      await verifyTask(taskId, { action, feedback });
      toast.success(`Task ${action}ed successfully`);
      loadData();
    } catch (error) {
      toast.error('Failed to verify task');
    }
  };

  const handleResubmit = async (taskId) => {
    const notes = prompt('Add notes about your changes:');
    try {
      await resubmitTask(taskId, { notes });
      toast.success('Task resubmitted for verification');
      loadData();
    } catch (error) {
      toast.error('Failed to resubmit task');
    }
  };

  const getProjectMembers = () => {
    if (!formData.project) return [];
    const selectedProject = projects.find(p => p.id === parseInt(formData.project));
    if (!selectedProject) return [];
    return users.filter(u => selectedProject.assigned_to?.includes(u.id));
  };

  const canUserEdit = (task) => {
    if (user?.role === 'admin') return true;
    if (user?.role === 'manager') return true;
    if (user?.role === 'member' && task.assigned_to === user?.id) return true;
    return false;
  };

  const canUserDelete = (task) => {
    if (user?.role === 'admin') return true;
    if (user?.role === 'manager') return true;
    return false;
  };

  return (
    <div className="tasks-container">
      <div className="page-header">
        <h1>Tasks</h1>
        {user?.role !== 'member' && (
          <button className="btn-add" onClick={() => setShowForm(true)}>+ Add Task</button>
        )}
      </div>

      {showForm && (
        <div className="modal">
          <div className="modal-content">
            <h2>{editingTask ? 'Edit Task' : 'Add New Task'}</h2>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Task Title *"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                required
              />
              <textarea
                placeholder="Description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                required
              />
              
              <label>Select Project *</label>
              <select
                value={formData.project}
                onChange={(e) => {
                  setFormData({ ...formData, project: e.target.value, assigned_to: '' });
                }}
                required
              >
                <option value="">Select Project</option>
                {projects.map(p => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
              
              <label>Assign To *</label>
              <select
                value={formData.assigned_to}
                onChange={(e) => setFormData({ ...formData, assigned_to: e.target.value })}
                required
                disabled={!formData.project}
              >
                <option value="">Select Member</option>
                {getProjectMembers().map(u => (
                  <option key={u.id} value={u.id}>{u.username} ({u.role})</option>
                ))}
              </select>
              
              <label>Priority</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="urgent">Urgent</option>
              </select>
              
              <label>Due Date *</label>
              <input
                type="date"
                value={formData.due_date}
                onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                required
              />
              
              <div className="modal-buttons">
                <button type="submit">Save</button>
                <button type="button" onClick={() => {
                  setShowForm(false);
                  setEditingTask(null);
                }}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="tasks-list">
        {tasks.map(task => (
          <div key={task.id} className="task-card">
            <div className="task-header">
              <h3>{task.title}</h3>
              <span className={`priority ${task.priority}`}>{task.priority}</span>
            </div>
            <p className="task-description">{task.description}</p>
            <div className="task-meta">
              <span>Project: {task.project_name}</span>
              <span>Assigned to: {task.assigned_to_name}</span>
              <span>Due: {task.due_date}</span>
            </div>
            
            <div className="task-status">
              <select 
                value={task.status} 
                onChange={(e) => handleStatusUpdate(task.id, e.target.value)} 
                className="status-select"
                disabled={!canUserEdit(task)}
              >
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
              <span className={`verification-badge ${task.verification_status}`}>
                {task.verification_status === 'unverified' && 'Pending Verification'}
                {task.verification_status === 'verified' && 'Verified'}
                {task.verification_status === 'rejected' && 'Rejected'}
              </span>
            </div>

            {task.manager_feedback && (
              <div className="feedback">Manager Feedback: {task.manager_feedback}</div>
            )}

            <div className="task-actions">
              {canUserEdit(task) && (
                <button className="btn-edit" onClick={() => handleEdit(task)}>Edit</button>
              )}
              
              {canUserDelete(task) && (
                <button className="btn-delete" onClick={() => handleDelete(task.id)}>Delete</button>
              )}
              
              {user?.role !== 'member' && task.status === 'completed' && task.verification_status === 'unverified' && (
                <>
                  <button className="btn-verify" onClick={() => handleVerify(task.id, 'approve')}>Approve</button>
                  <button className="btn-reject" onClick={() => handleVerify(task.id, 'reject')}>Reject</button>
                </>
              )}
              
              {user?.role === 'member' && task.verification_status === 'rejected' && (
                <button className="btn-resubmit" onClick={() => handleResubmit(task.id)}>Resubmit</button>
              )}
            </div>
          </div>
        ))}
        {tasks.length === 0 && <p className="no-data">No tasks found</p>}
      </div>
    </div>
  );
};

export default Tasks;
