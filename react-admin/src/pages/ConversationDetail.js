import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  CardHeader,
  Divider,
  Chip,
  TextField,
  Button,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Avatar,
} from '@mui/material';
import { Send as SendIcon, ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getConversation, sendMessage } from '../services/api';
import { format } from 'date-fns';

function ConversationDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [conversation, setConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newMessage, setNewMessage] = useState('');
  const [sending, setSending] = useState(false);

  useEffect(() => {
    fetchConversation();
  }, [id]);

  const fetchConversation = async () => {
    try {
      setLoading(true);
      const response = await getConversation(id);
      setConversation(response.data.conversation);
      setMessages(response.data.messages || []);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching conversation:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim() || !conversation) return;
    
    try {
      setSending(true);
      await sendMessage(conversation.telegram_chat_id, newMessage);
      setNewMessage('');
      // Refresh conversation after sending
      await fetchConversation();
    } catch (err) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

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
        Error loading conversation: {error}
        <Button onClick={fetchConversation} sx={{ ml: 2 }}>Retry</Button>
      </Alert>
    );
  }

  if (!conversation) {
    return (
      <Alert severity="warning">Conversation not found</Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        <IconButton onClick={() => navigate('/conversations')}>
          <ArrowBackIcon />
        </IconButton>
        <Typography variant="h4">Conversation #{id}</Typography>
      </Box>

      <Card sx={{ mb: 3 }}>
        <CardHeader
          title={`Chat: ${conversation.telegram_chat_id}`}
          subheader={
            <Box display="flex" alignItems="center" gap={2}>
              <Typography>Customer: {conversation.customer_id}</Typography>
              <Chip
                label={conversation.language?.toUpperCase() || 'EN'}
                size="small"
              />
              {conversation.needs_human && (
                <Chip label="Needs Human" color="error" size="small" />
              )}
            </Box>
          }
        />
        <CardContent>
          <Typography variant="body2" color="text.secondary">
            Created: {format(new Date(conversation.created_at), 'PPpp')}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Last updated: {format(new Date(conversation.updated_at), 'PPpp')}
          </Typography>
        </CardContent>
      </Card>

      <Card sx={{ mb: 3, flexGrow: 1 }}>
        <CardHeader title="Messages" />
        <CardContent sx={{ p: 0 }}>
          <List>
            {messages.length === 0 ? (
              <ListItem>
                <ListItemText primary="No messages yet" />
              </ListItem>
            ) : (
              messages.map((msg) => (
                <React.Fragment key={msg.id}>
                  <ListItem>
                    <Box display="flex" gap={2} width="100%">
                      <Avatar sx={{
                        bgcolor: msg.is_from_customer ? 'primary.main' : 'success.main',
                        width: 36,
                        height: 36,
                        fontSize: '0.75rem',
                      }}>
                        {msg.is_from_customer ? 'C' : 'A'}
                      </Avatar>
                      <Box flexGrow={1}>
                        <Box display="flex" alignItems="center" gap={1} mb={0.5}>
                          <Typography fontWeight="bold">
                            {msg.is_from_customer ? 'Customer' : 'Assistant'}
                          </Typography>
                          <Chip
                            label={msg.language?.toUpperCase() || 'EN'}
                            size="small"
                          />
                          <Typography variant="caption" color="text.secondary">
                            {format(new Date(msg.created_at), 'PPpp')}
                          </Typography>
                        </Box>
                        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                          {msg.content}
                        </Typography>
                      </Box>
                    </Box>
                  </ListItem>
                  <Divider component="li" />
                </React.Fragment>
              ))
            )}
          </List>
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Box display="flex" gap={2} alignItems="flex-end">
            <TextField
              fullWidth
              multiline
              rows={2}
              placeholder="Type a message..."
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={sending}
            />
            <IconButton
              color="primary"
              onClick={handleSendMessage}
              disabled={sending || !newMessage.trim()}
            >
              <SendIcon />
            </IconButton>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}

export default ConversationDetail;
