import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import Navbar from '../components/Navbar';
import StatsCards from '../components/StatsCards';
import ProjectCard from '../components/ProjectCard';
import TaskCard from '../components/TaskCard';
import ProjectModal from '../components/ProjectModal';
import TaskModal from '../components/TaskModal';
import './Dashboard.css';

function Dashboard() {
    const [stats, setStats] = useState(null);
    const [projects, setProjects] = useState([]);
    const [tasks, setTasks] = useState([]);
    const [activeTab, setActiveTab] = useState('dashboard');
    const [userRole, setUserRole] = useState('');
    const [userName, setUserName] = useState('');
    const [loading, setLoading] = useState(true);
    const [showProjectModal, setShowProjectModal] = useState(false);
    const [showTaskModal, setShowTaskModal] = useState(false);
    const [editingProject, setEditingProject] = useState(null);
    const [editingTask, setEditingTask] = useState(null);
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();

    const canEdit = userRole === 'admin' || userRole === 'manager';

    useEffect(() => {
        loadUserRole();
        loadUsers();
        loadData();
    }, []);

    const loadUserRole = async () => {
        try {
            const response = await api.get('/users/profile/');
            setUserRole(response.data.role);
            setUserName(response.data.username);
            setLoading(false);
        } catch (error) {
            setLoading(false);
            if (error.response?.status === 401) navigate('/login');
        }
    };

    const loadUsers = async () => {
        try {
            const response = await api.get('/users/');
            setUsers(response.data);
        } catch (error) {
            console.error('Error loading users');
        }
    };

    const loadData = async () => {
        try {
            const [statsRes, projectsRes, tasksRes] = await Promise.all([
                api.get('/dashboard/stats/'),
                api.get('/projects/'),
                api.get('/tasks/')
            ]);
            setStats(statsRes.data);
            setProjects(projectsRes.data);
            setTasks(tasksRes.data);
        } catch (error) {
            console.error('Error loading data');
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    const handleCreateProject = async (projectData) => {
        try {
            if (editingProject) {
                await api.put(`/projects/${editingProject.id}/`, projectData);
            } else {
                await api.post('/projects/', projectData);
            }
            setShowProjectModal(false);
            setEditingProject(null);
            loadData();
        } catch (error) {
            alert('Error saving project');
        }
    };

    const handleDeleteProject = async (projectId) => {
        if (window.confirm('Delete this project?')) {
            try {
                await api.delete(`/projects/${projectId}/`);
                loadData();
            } catch (error) {
                alert('Error deleting project');
            }
        }
    };

    const handleCreateTask = async (taskData) => {
        try {
            if (editingTask) {
                await api.put(`/tasks/${editingTask.id}/`, taskData);
            } else {
                await api.post('/tasks/', taskData);
            }
            setShowTaskModal(false);
            setEditingTask(null);
            loadData();
        } catch (error) {
            alert('Error saving task');
        }
    };

    const handleDeleteTask = async (taskId) => {
        if (window.confirm('Delete this task?')) {
            try {
                await api.delete(`/tasks/${taskId}/`);
                loadData();
            } catch (error) {
                alert('Error deleting task');
            }
        }
    };

    const handleUpdateTaskStatus = async (taskId, newStatus) => {
        try {
            await api.patch(`/tasks/${taskId}/`, { status: newStatus });
            loadData();
        } catch (error) {
            alert('Error updating status');
        }
    };

    if (loading) return <div className="loading">Loading...</div>;

    return (
        <div className="dashboard">
            <Navbar 
                activeTab={activeTab} 
                setActiveTab={setActiveTab}
                userName={userName}
                userRole={userRole}
                onLogout={handleLogout}
            />

            <div className="main-content">
                {activeTab === 'dashboard' && (
                    <>
                        <div className="header">
                            <div>
                                <h1>Welcome back, {userName}! </h1>
                            </div> 
                        </div>
                        {stats && <StatsCards stats={stats} />}

                        <div className="projects-section">
                            <h2>Recent Projects</h2>
                            <div className="projects-list">
                                {projects.slice(0, 3).map(project => (
                                    <ProjectCard
                                        key={project.id}
                                        project={project}
                                        showButtons={false}
                                    />
                                ))}
                            </div>
                        </div>
                    </>
                )}

                {activeTab === 'projects' && (
                    <>
                        <div className="header">
                            <h1>Projects</h1>
                            {canEdit && (
                                <button className="btn-primary" onClick={() => setShowProjectModal(true)}>
                                    + New Project
                                </button>
                            )}
                        </div>
                        <div className="projects-list">
                            {projects.map(project => (
                                <ProjectCard
                                    key={project.id}
                                    project={project}
                                    showButtons={canEdit}
                                    onEdit={(p) => {
                                        setEditingProject(p);
                                        setShowProjectModal(true);
                                    }}
                                    onDelete={handleDeleteProject}
                                />
                            ))}
                        </div>
                    </>
                )}

                {activeTab === 'tasks' && (
                    <>
                        <div className="header">
                            <h1>Tasks</h1>
                            {canEdit && (
                                <button className="btn-primary" onClick={() => setShowTaskModal(true)}>
                                    + New Task
                                </button>
                            )}
                        </div>
                        <div className="tasks-list">
                            {tasks.map(task => (
                                <TaskCard
                                    key={task.id}
                                    task={task}
                                    showButtons={canEdit}
                                    onEdit={(t) => {
                                        setEditingTask(t);
                                        setShowTaskModal(true);
                                    }}
                                    onDelete={handleDeleteTask}
                                    onStatusChange={handleUpdateTaskStatus}
                                />
                            ))}
                        </div>
                    </>
                )}
            </div>

            <ProjectModal
                isOpen={showProjectModal}
                project={editingProject}
                userRole={userRole}
                users={users}
                onClose={() => {
                    setShowProjectModal(false);
                    setEditingProject(null);
                }}
                onSave={handleCreateProject}
            />

            <TaskModal
                isOpen={showTaskModal}
                task={editingTask}
                projects={projects}
                users={users}
                onClose={() => {
                    setShowTaskModal(false);
                    setEditingTask(null);
                }}
                onSave={handleCreateTask}
            />
        </div>
    );
}

export default Dashboard;