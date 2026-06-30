import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  CardHeader,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Chip,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { getServices } from '../services/api';

function Services() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [currentService, setCurrentService] = useState(null);

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const response = await getServices();
      setServices(response.data.services || []);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching services:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenDialog = (service = null) => {
    setCurrentService(service || {
      name: '',
      price: 0,
      description: '',
      amharicName: '',
      amharicDescription: '',
    });
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setCurrentService(null);
  };

  const handleSave = () => {
    // In a real app, you would call the API here
    console.log('Saving service:', currentService);
    handleCloseDialog();
    fetchServices();
  };

  const handleDelete = (id) => {
    // In a real app, you would call the API here
    console.log('Deleting service:', id);
    fetchServices();
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
        Error loading services: {error}
        <Button onClick={fetchServices} sx={{ ml: 2 }}>Retry</Button>
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Services</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Service
        </Button>
      </Box>

      <Card>
        <CardContent sx={{ p: 0 }}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Amharic Name</TableCell>
                  <TableCell>Price (ETB)</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {services.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      No services found
                    </TableCell>
                  </TableRow>
                ) : (
                  services.map((service) => (
                    <TableRow key={service.id}>
                      <TableCell>
                        <Typography fontWeight="bold">{service.name}</Typography>
                      </TableCell>
                      <TableCell>{service.amharicName || '-'}</TableCell>
                      <TableCell>
                        <Chip
                          label={`ETB ${service.price?.toLocaleString()}`}
                          color="primary"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>{service.description}</TableCell>
                      <TableCell>
                        <IconButton
                          size="small"
                          onClick={() => handleOpenDialog(service)}
                        >
                          <EditIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDelete(service.id)}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Service Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="md" fullWidth>
        <DialogTitle>
          {currentService?.id ? 'Edit Service' : 'Add New Service'}
        </DialogTitle>
        <DialogContent>
          <Box display="flex" gap={2} mt={2}>
            <TextField
              fullWidth
              label="Name (English)"
              value={currentService?.name || ''}
              onChange={(e) => 
                setCurrentService({ ...currentService, name: e.target.value })
              }
            />
            <TextField
              fullWidth
              label="Name (Amharic)"
              value={currentService?.amharicName || ''}
              onChange={(e) => 
                setCurrentService({ ...currentService, amharicName: e.target.value })
              }
            />
          </Box>
          <Box display="flex" gap={2} mt={2}>
            <TextField
              fullWidth
              label="Price (ETB)"
              type="number"
              value={currentService?.price || 0}
              onChange={(e) => 
                setCurrentService({ ...currentService, price: parseFloat(e.target.value) || 0 })
              }
            />
          </Box>
          <Box display="flex" gap={2} mt={2}>
            <TextField
              fullWidth
              label="Description (English)"
              multiline
              rows={3}
              value={currentService?.description || ''}
              onChange={(e) => 
                setCurrentService({ ...currentService, description: e.target.value })
              }
            />
            <TextField
              fullWidth
              label="Description (Amharic)"
              multiline
              rows={3}
              value={currentService?.amharicDescription || ''}
              onChange={(e) => 
                setCurrentService({ ...currentService, amharicDescription: e.target.value })
              }
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSave} variant="contained" color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Services;
