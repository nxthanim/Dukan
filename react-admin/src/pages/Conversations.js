import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Divider,
  Chip,
  TextField,
  InputAdornment,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Search as SearchIcon, Refresh as RefreshIcon } from '@mui/icons-material';
import { Link, useNavigate } from 'react-router-dom';
import { getConversations } from '../services/api';
import { formatDistanceToNow } from 'date-fns';

function Conversations() {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState('all'); // 'all', 'needs-human', 'recent'
  const navigate = useNavigate();

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      setLoading(true);
      const response = await getConversations();
      setConversations(response.data.conversations || []);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching conversations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    fetchConversations();
  };

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
  };

  const filteredConversations = conversations
    .filter((conv) => {
      // Filter by search
      const matchesSearch = 
        conv.telegram_chat_id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        conv.customer_id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        searchQuery === '';
      
      // Filter by type
      const matchesFilter = filter === 'all' ||
        (filter === 'needs-human' && conv.needs_human) ||
        (filter === 'recent' && isRecent(conv.updated_at));
      
      return matchesSearch && matchesFilter;
    })
    .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));

  const isRecent = (dateString) => {
    if (!dateString) return false;
    const date = new Date(dateString);
    const now = new Date();
    const hoursDiff = (now - date) / (1000 * 60 * 60);
    return hoursDiff <= 24; // Last 24 hours
  };

  const needsHumanCount = conversations.filter(c => c.needs_human).length;

  if (loading && conversations.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Error loading conversations: {error}
        <Button onClick={fetchConversations} sx={{ ml: 2 }}>Retry</Button>
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Conversations</Typography>
        <Box display="flex" alignItems="center" gap={2}>
          <TextField
            size="small"
            placeholder="Search chats..."
            value={searchQuery}
            onChange={handleSearch}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            sx={{ width: 250 }}
          />
          <IconButton onClick={handleRefresh} color="primary">
            <RefreshIcon />
          </IconButton>
        </Box>
      </Box>

      <Box display="flex" gap={1} mb={3}>
        <Chip
          label={`All (${conversations.length})`}
          color={filter === 'all' ? 'primary' : 'default'}
          onClick={() => setFilter('all')}
          clickable
        />
        <Chip
          label={`Needs Human (${needsHumanCount})`}
          color={filter === 'needs-human' ? 'error' : 'default'}
          onClick={() => setFilter('needs-human')}
          clickable
        />
        <Chip
          label="Recent (24h)"
          color={filter === 'recent' ? 'success' : 'default'}
          onClick={() => setFilter('recent')}
          clickable
        />
      </Box>

      {filteredConversations.length === 0 ? (
        <Alert severity="info">No conversations found</Alert>
      ) : (
        <Card>
          <CardContent sx={{ p: 0 }}>
            <List>
              {filteredConversations.map((conv) => (
                <React.Fragment key={conv.id}>
                  <ListItem disablePadding>
                    <ListItemButton
                      component={Link}
                      to={`/conversations/${conv.id}`}
                      sx={{ py: 2 }}
                    >
                      <Box display="flex" flexDirection="column" flexGrow={1}>
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography fontWeight="bold">
                            {conv.telegram_chat_id}
                          </Typography>
                          {conv.needs_human && (
                            <Chip
                              label="Needs Human"
                              color="error"
                              size="small"
                            />
                          )}
                        </Box>
                        <Typography variant="body2" color="text.secondary">
                          Customer: {conv.customer_id}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Language: {conv.language?.toUpperCase()}
                        </Typography>
                      </Box>
                      <Box textAlign="right">
                        <Typography variant="body2" color="text.secondary">
                          {formatDistanceToNow(new Date(conv.updated_at), { addSuffix: true })}
                        </Typography>
                      </Box>
                    </ListItemButton>
                  </ListItem>
                  <Divider component="li" />
                </React.Fragment>
              ))}
            </List>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}

export default Conversations;
