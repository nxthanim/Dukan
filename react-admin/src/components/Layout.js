import React, { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import {
  Drawer,
  Box,
  Toolbar,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  AppBar,
  Typography,
  IconButton,
  Badge,
  CssBaseline,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Chat as ChatIcon,
  ShoppingCart as ShoppingCartIcon,
  Settings as SettingsIcon,
  Menu as MenuIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { text: 'Conversations', icon: <ChatIcon />, path: '/conversations' },
  { text: 'Services', icon: <BusinessIcon />, path: '/services' },
  { text: 'Orders', icon: <ShoppingCartIcon />, path: '/orders' },
];

function Layout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [needsHumanCount, setNeedsHumanCount] = useState(0);
  const navigate = useNavigate();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleMenuClick = (path) => {
    navigate(path);
    setMobileOpen(false);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            🏪 Dukan Admin
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          <SidebarContent onMenuClick={handleMenuClick} needsHumanCount={needsHumanCount} />
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          <SidebarContent onMenuClick={handleMenuClick} needsHumanCount={needsHumanCount} />
        </Drawer>
      </Box>
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          background: '#f5f7fa',
          minHeight: '100vh',
        }}
      >
        <Toolbar />
        <Outlet context={{ setNeedsHumanCount }} />
      </Box>
    </Box>
  );
}

function SidebarContent({ onMenuClick, needsHumanCount }) {
  return (
    <div>
      <Toolbar />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton onClick={() => onMenuClick(item.path)}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
              {item.text === 'Conversations' && needsHumanCount > 0 && (
                <Badge
                  badgeContent={needsHumanCount}
                  color="error"
                  sx={{ ml: 2 }}
                />
              )}
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </div>
  );
}

export default Layout;
