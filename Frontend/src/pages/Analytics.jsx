import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, Legend } from 'recharts';
import { Activity, CheckCircle, Target, BarChart2 } from 'lucide-react';
import StatCard from '../components/common/StatCard';
import Card from '../components/common/Card';
import { api } from '../api';

const Analytics = () => {
    const [trendData, setTrendData] = useState([]);
    const [distributionData, setDistributionData] = useState([]);
    const [stats, setStats] = useState({
        total_runs: 0,
        pass_rate: 0,
        avg_reward: 0,
        coverage: 'N/A'
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const historyRes = await api.getHistory();
                const history = historyRes.data.history || [];

                processHistoryData(history);
            } catch (error) {
                console.error("Failed to fetch analytics data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const processHistoryData = (history) => {
        // 1. Calculate Top Stats
        const totalRuns = history.length;
        const passedRuns = history.filter(h => h.status === 'passed').length;
        const passRate = totalRuns > 0 ? ((passedRuns / totalRuns) * 100).toFixed(1) : 0;

        const rewards = history.filter(h => h.reward !== undefined).map(h => h.reward);
        const avgReward = rewards.length > 0 ? (rewards.reduce((a, b) => a + b, 0) / rewards.length).toFixed(1) : 0;

        setStats({
            total_runs: totalRuns,
            pass_rate: passRate,
            avg_reward: avgReward,
            coverage: 'N/A' // Backend doesn't provide this yet
        });

        // 2. Process Trend Data (Group by Date)
        const trends = {};
        // Sort history by date ascending for the chart
        const sortedHistory = [...history].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

        sortedHistory.forEach(run => {
            const date = new Date(run.timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            if (!trends[date]) {
                trends[date] = { date, passed: 0, failed: 0 };
            }
            if (run.status === 'passed') {
                trends[date].passed += 1;
            } else {
                trends[date].failed += 1;
            }
        });
        setTrendData(Object.values(trends));

        // 3. Process Distribution Data
        setDistributionData([
            { name: 'Passed', value: passedRuns, color: '#22c55e' },
            { name: 'Failed', value: totalRuns - passedRuns, color: '#ef4444' },
        ]);
    };

    return (
        <div className="space-y-6 animate-fade-in">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Analytics & Reports</h1>
                <p className="text-muted-foreground mt-1">Deep dive into your testing metrics.</p>
            </div>

            {/* Top Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard title="Total Tests" value={stats.total_runs.toString()} icon={Activity} trend={null} trendValue={null} color="blue" />
                <StatCard title="Pass Rate" value={`${stats.pass_rate}%`} icon={CheckCircle} trend={null} trendValue={null} color="green" />
                <StatCard title="Avg Reward" value={stats.avg_reward.toString()} icon={Target} trend={null} trendValue={null} color="purple" />
                <StatCard title="Coverage" value={stats.coverage} icon={BarChart2} trend={null} trendValue={null} color="orange" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Test Execution Trends */}
                <Card>
                    <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                        <Activity className="h-5 w-5 text-blue-500" />
                        Test Execution Trends
                    </h3>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={trendData}>
                                <defs>
                                    <linearGradient id="colorFailed" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                                    </linearGradient>
                                    <linearGradient id="colorPassed" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                                <XAxis dataKey="date" stroke="#666" tick={{ fill: '#666' }} axisLine={false} tickLine={false} />
                                <YAxis stroke="#666" tick={{ fill: '#666' }} axisLine={false} tickLine={false} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#13131f', borderColor: '#333', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff' }}
                                />
                                <Area type="monotone" dataKey="failed" stroke="#ef4444" fillOpacity={1} fill="url(#colorFailed)" />
                                <Area type="monotone" dataKey="passed" stroke="#22c55e" fillOpacity={1} fill="url(#colorPassed)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </Card>

                {/* Test Distribution */}
                <Card>
                    <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                        <PieChart className="h-5 w-5 text-purple-500" />
                        Test Distribution
                    </h3>
                    <div className="h-[300px] w-full flex items-center justify-center">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={distributionData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={80}
                                    outerRadius={100}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {distributionData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#13131f', borderColor: '#333', borderRadius: '8px' }}
                                    itemStyle={{ color: '#fff' }}
                                />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </Card>
            </div>

            {/* 
                NOTE: Coverage and Performance charts hidden as backend does not currently provide this data.
                To re-enable, backend needs to return 'coverage_data' and 'performance_metrics'.
            */}
        </div>
    );
};

export default Analytics;
