import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, CheckCircle, Play, Upload, Zap, BarChart2, FileText } from 'lucide-react';
import StatCard from '../components/common/StatCard';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

const Dashboard = () => {
    const navigate = useNavigate();
    const [stats, setStats] = useState({
        total_runs: 0,
        passed_runs: 0,
        avg_reward: 0,
        active_projects: 0
    });
    const [recentActivity, setRecentActivity] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [statsRes, historyRes] = await Promise.all([
                    api.getDashboardStats(),
                    api.getHistory()
                ]);

                setStats(statsRes.data);

                // Process history for recent activity
                const history = historyRes.data.history || [];
                const activity = history.slice(0, 5).map((run, index) => ({
                    id: index,
                    type: run.status === 'passed' ? 'success' : 'warning',
                    message: `Test run ${run.status}: ${run.project_name}`,
                    time: new Date(run.timestamp).toLocaleString()
                }));
                setRecentActivity(activity);
            } catch (error) {
                console.error("Failed to fetch dashboard data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const statCards = [
        { title: 'Total Test Runs', value: stats.total_runs.toString(), icon: Activity, trend: null, trendValue: null, color: 'blue' },
        { title: 'Passed Tests', value: stats.passed_runs.toString(), icon: CheckCircle, trend: null, trendValue: null, color: 'green' },
        { title: 'Average Reward', value: stats.avg_reward.toFixed(2), icon: Zap, trend: null, trendValue: null, color: 'purple' },
        { title: 'Active Projects', value: stats.active_projects.toString(), icon: FileText, trend: null, trendValue: null, color: 'orange' },
    ];

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                    <p className="text-muted-foreground mt-1">Monitor your testing infrastructure at a glance</p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" size="sm" onClick={() => navigate('/settings')}>
                        Settings
                    </Button>
                    <Button size="sm" onClick={() => navigate('/generate')}>
                        <Zap className="mr-2 h-4 w-4" />
                        New Test Run
                    </Button>
                </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {statCards.map((stat, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                    >
                        <StatCard {...stat} />
                    </motion.div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Recent Activity */}
                <div className="lg:col-span-2">
                    <Card className="h-full">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="text-lg font-semibold flex items-center gap-2">
                                <Activity className="h-5 w-5 text-blue-500" />
                                Recent Activity
                            </h3>
                            <Button variant="ghost" size="sm" className="text-xs" onClick={() => navigate('/results')}>View All</Button>
                        </div>
                        <div className="space-y-4">
                            {recentActivity.length === 0 ? (
                                <p className="text-muted-foreground text-sm">No recent activity found.</p>
                            ) : (
                                recentActivity.map((activity, index) => (
                                    <div key={activity.id} className="flex items-start gap-4 p-4 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                                        <div className={`mt-1 p-2 rounded-full ${activity.type === 'success' ? 'bg-green-500/20 text-green-500' :
                                            activity.type === 'warning' ? 'bg-red-500/20 text-red-500' :
                                                'bg-blue-500/20 text-blue-500'
                                            }`}>
                                            {activity.type === 'success' ? <CheckCircle className="h-4 w-4" /> :
                                                <Activity className="h-4 w-4" />}
                                        </div>
                                        <div className="flex-1">
                                            <p className="font-medium text-sm">{activity.message}</p>
                                            <p className="text-xs text-muted-foreground mt-1">{activity.time}</p>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </Card>
                </div>

                {/* Quick Actions */}
                <div>
                    <Card className="h-full">
                        <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                            <Zap className="h-5 w-5 text-yellow-500" />
                            Quick Actions
                        </h3>
                        <div className="space-y-3">
                            <Button variant="secondary" className="w-full justify-start bg-green-600 hover:bg-green-700 text-white" onClick={() => navigate('/upload')}>
                                <Upload className="mr-2 h-4 w-4" />
                                Upload Project
                            </Button>
                            <Button variant="secondary" className="w-full justify-start bg-blue-600 hover:bg-blue-700 text-white" onClick={() => navigate('/generate')}>
                                <Zap className="mr-2 h-4 w-4" />
                                Generate Tests
                            </Button>
                            <Button variant="secondary" className="w-full justify-start" onClick={() => navigate('/run')}>
                                <Play className="mr-2 h-4 w-4" />
                                Run Tests
                            </Button>
                            <Button variant="secondary" className="w-full justify-start" onClick={() => navigate('/analytics')}>
                                <BarChart2 className="mr-2 h-4 w-4" />
                                Analytics
                            </Button>
                            <Button variant="secondary" className="w-full justify-start" onClick={() => navigate('/results')}>
                                <FileText className="mr-2 h-4 w-4" />
                                View Reports
                            </Button>
                        </div>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
