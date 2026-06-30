import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import { Link } from 'react-router-dom';
import { getConversations, getStats } from '../services/api';
import {
  Chat as ChatIcon,
  Warning as WarningIcon,
  ShoppingCart as ShoppingCartIcon,
  AttachMoney as AttachMoneyIcon,
} from '@mui/icons-material';

const statCards = [
  {
    title: 'Total Conversations',
    icon: <ChatIcon fontSize="large" color="primary" />,
    color: '#1976d2',
    key: 'totalConversations',
    link: '/conversations',
    linkText: 'View all',
  },
  {
    title: 'Needs Human',
    icon: <WarningIcon fontSize="large" color="error" />,
    color: '#d32f2f',
    key: 'needsHuman',
    link: '/conversations',
    linkText: 'Review now',
  },
  {
    title: 'Total Orders',
    icon: <ShoppingCartIcon fontSize="large" color="success" />,
    color: '#4caf50',
    key: 'totalOrders',
    link: '/orders',
    linkText: 'View orders',
  },
  {
    title: 'Total Revenue',
    icon: <AttachMoneyIcon fontSize="large" color="secondary" />,
    color: '#9c27b0',
    key: 'totalRevenue',
    link: '/orders',
    linkText: 'View details',
    format: (value) => `ETB ${value?.toLocaleString() || '0'}`,
  },
];

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [recentConversations, setRecentConversations] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch stats
        const statsResponse = await getStats();
        setStats(statsResponse.data);
        
        // Fetch recent conversations
        const convResponse = await getConversations();
        setRecentConversations(convResponse.data.conversations?.slice(0, 5) || []);
        
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Error loading dashboard: {error}
        <Button onClick={() => window.location.reload()} sx={{ ml: 2 }}>Retry</Button>
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Welcome to Dukan Admin Panel
      </Typography>
      
      <Grid container spacing={3} sx={{ mt: 2 }}>
        {statCards.map((card) => (
          <Grid item xs={12} sm={6} lg={3} key={card.key}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  {card.icon}
                  <Typography variant="h6" sx={{ ml: 1, flexGrow: 1 }}>
                    {card.title}
                  </Typography>
                </Box>
                <Typography variant="h3" component="div" sx={{ fontWeight: 'bold' }}>
                  {card.format ? card.format(stats?.[card.key]) : stats?.[card.key] || 0}
                </Typography>
                <Button
                  component={Link}
                  to={card.link}
                  variant="text"
                  size="small"
                  sx={{ mt: 1 }}
                >
                  {card.linkText}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recent Conversations
          </Typography>
          {recentConversations.length === 0 ? (
            <Typography color="text.secondary">No conversations yet</Typography>
          ) : (
            recentConversations.map((conv) => (
              <Box
                key={conv.id}
                display="flex"
                alignItems="center"
                p={2}
                borderBottom="1px solid #eee"
                sx={{ '&:last-child': { borderBottom: 'none' } }}
              >
                <Box flexGrow={1}>
                  <Typography fontWeight="bold">
                    Chat: {conv.telegram_chat_id}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Customer: {conv.customer_id} | Language: {conv.language}
                  </Typography>
                </Box>
                {conv.needs_human && (
                  <Box
                    bgcolor="error.light"
                    color="error.contrastText"
                    px={2}
                    py={1}
                    borderRadius={1}
                    fontSize="0.75rem"
                    fontWeight="bold"
                  >
                    NEEDS HUMAN
                  </Box>
                )}
              </Box>
            ))
          )}
        </CardContent>
      </Card>
    </Box>
  );
}

export default Dashboard;
