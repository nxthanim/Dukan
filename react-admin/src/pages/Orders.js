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
  Chip,
  TextField,
  InputAdornment,
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { getOrders } from '../services/api';
import { format } from 'date-fns';

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await getOrders();
      setOrders(response.data.orders || []);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching orders:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredOrders = orders
    .filter((order) => {
      const matchesSearch = 
        order.customer_id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        order.service_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        searchQuery === '';
      return matchesSearch;
    })
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

  const totalRevenue = filteredOrders.reduce((sum, order) => sum + (order.price || 0), 0);

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
        Error loading orders: {error}
        <Button onClick={fetchOrders} sx={{ ml: 2 }}>Retry</Button>
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">Orders</Typography>
        <Chip
          label={`Total Revenue: ETB ${totalRevenue.toLocaleString()}`}
          color="success"
          variant="outlined"
        />
      </Box>

      <TextField
        fullWidth
        size="small"
        placeholder="Search orders..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
        sx={{ mb: 3 }}
      />

      <Card>
        <CardHeader title={`Total Orders: ${filteredOrders.length}`} />
        <CardContent sx={{ p: 0 }}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Date</TableCell>
                  <TableCell>Customer</TableCell>
                  <TableCell>Service</TableCell>
                  <TableCell>Quantity</TableCell>
                  <TableCell>Price (ETB)</TableCell>
                  <TableCell>Total (ETB)</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredOrders.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      No orders found
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredOrders.map((order) => (
                    <TableRow key={order.id}>
                      <TableCell>
                        {format(new Date(order.created_at), 'PP')}
                      </TableCell>
                      <TableCell>{order.customer_id}</TableCell>
                      <TableCell>{order.service_name}</TableCell>
                      <TableCell>
                        <Chip label={order.quantity} variant="outlined" />
                      </TableCell>
                      <TableCell>ETB {order.price?.toLocaleString()}</TableCell>
                      <TableCell>
                        <Chip
                          label={`ETB ${(order.price * order.quantity).toLocaleString()}`}
                          color="success"
                          variant="outlined"
                        />
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
}

export default Orders;
