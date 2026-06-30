# Dukan Admin - React Dashboard

A beautiful React admin dashboard for monitoring your Dukan Telegram bot.

## Features

- **Real-time Dashboard** - View stats at a glance
- **Conversation Management** - List, filter, and view all conversations
- **Service Catalog** - Manage your printing services
- **Order Tracking** - View all orders and revenue
- **Responsive Design** - Works on desktop and mobile
- **Real-time Updates** - WebSocket integration for live updates

## Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Running Dukan Python backend (port 8000)

### Installation

```bash
# Navigate to react-admin directory
cd react-admin

# Install dependencies
npm install

# Start development server
npm start
```

The admin dashboard will be available at: http://localhost:3000

### Configuration

Create a `.env` file in the `react-admin` directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_PORT=8000
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm run build` - Builds the app for production
- `npm test` - Runs tests
- `npm run eject` - Ejects from Create React App

## Connecting to Backend

The React app connects to your Python Dukan backend at `http://localhost:8000` by default.

### Production Deployment

1. Build the app:
```bash
npm run build
```

2. Serve the build folder with any static server (nginx, Apache, etc.)

3. Configure CORS in your Python backend if needed

## Project Structure

```
react-admin/
├── public/              # Static files
├── src/
│   ├── components/      # Reusable components
│   │   └── Layout.js    # Main layout with sidebar
│   ├── pages/           # Page components
│   │   ├── Dashboard.js
│   │   ├── Conversations.js
│   │   ├── ConversationDetail.js
│   │   ├── Services.js
│   │   └── Orders.js
│   ├── services/        # API services
│   │   └── api.js       # API client
│   ├── App.js           # Main app router
│   ├── index.js         # Entry point
│   └── index.css        # Global styles
├── package.json
└── README.md
```

## API Endpoints Used

- `GET /conversations` - List all conversations
- `GET /conversations/{id}/messages` - Get conversation messages
- `GET /api/services` - List all services
- `GET /api/orders` - List all orders
- `GET /api/stats` - Get dashboard statistics
- `POST /api/send-message` - Send message to conversation
- `POST /conversations/{id}/flag` - Flag conversation
- `ws://localhost:8000/ws` - WebSocket for real-time updates

## Customization

### Changing Colors

Edit the theme in `src/App.js`:

```javascript
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',  // Change primary color
    },
    // ... other colors
  },
});
```

### Adding New Pages

1. Create a new file in `src/pages/`
2. Add a route in `src/App.js`
3. Add a menu item in `src/components/Layout.js`

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## License

MIT License
