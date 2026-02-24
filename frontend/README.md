# InnovatEPAM Frontend

React frontend for InnovatEPAM Portal.

## Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite 5
- **Language**: TypeScript
- **Routing**: React Router 6
- **HTTP Client**: Axios
- **Testing**: Vitest (unit), Playwright (e2e)
- **Code Quality**: ESLint, Prettier

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API client and services
│   ├── components/       # React components
│   │   ├── auth/        # Authentication components
│   │   ├── ideas/       # Idea components
│   │   ├── admin/       # Admin components
│   │   ├── common/      # Shared components
│   │   └── routing/     # Route guards
│   ├── contexts/        # React contexts (auth, etc.)
│   ├── hooks/           # Custom hooks
│   ├── pages/           # Page components
│   │   ├── auth/       # Auth pages
│   │   ├── ideas/      # Idea pages
│   │   └── admin/      # Admin pages
│   ├── App.tsx          # Root component
│   ├── routes.tsx       # Route configuration
│   └── main.tsx         # Entry point
├── tests/
│   ├── unit/            # Unit tests
│   └── e2e/            # End-to-end tests
│       ├── auth/       # Auth flow tests
│       ├── ideas/      # Idea flow tests
│       └── admin/      # Admin flow tests
├── package.json
├── vite.config.ts
├── vitest.config.ts
└── playwright.config.ts
```

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Create `.env` file**:
   ```bash
   cp .env.example .env
   ```

3. **Configure environment variables** in `.env`:
   - `VITE_API_BASE_URL`: Backend API URL (default: http://localhost:8000)

4. **Start development server**:
   ```bash
   npm run dev
   ```

   App runs at: http://localhost:3000

## Development

### Running Tests

```bash
# Unit tests
npm run test

# Unit tests with UI
npm run test:ui

# Unit tests with coverage
npm run test:coverage

# End-to-end tests
npm run test:e2e

# End-to-end tests with UI
npm run test:e2e:ui

# End-to-end tests debug mode
npm run test:e2e:debug
```

### Code Quality

```bash
# Lint
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Check formatting
npm run format:check
```

### Build

```bash
# Production build
npm run build

# Preview production build
npm run preview
```

## Architecture

### Authentication Flow

1. User logs in → receives access token (15 min) and refresh token (7 days)
2. Access token stored in localStorage
3. Refresh token stored in HTTP-only cookie
4. API client automatically adds Bearer token to requests
5. On 401 error, automatically refresh access token
6. On refresh failure, redirect to login

### State Management

- **AuthContext**: User authentication state (user, isAuthenticated, login, logout)
- Local component state for UI
- API calls via axios client with interceptors

### Routing

- **Public routes**: `/`, `/login`, `/register`
- **Protected routes**: `/dashboard`, `/ideas/*`, `/admin/*`
- Route guards check authentication status
- Redirects to `/login` if not authenticated

## Components

Components follow these principles:
- **Functional components** with hooks
- **TypeScript** for type safety
- **Single responsibility** (< 30 lines per function per constitution)
- **Prop validation** with TypeScript interfaces
- **Accessible** (ARIA labels, semantic HTML)

## Testing

Following the project constitution:
- **Unit tests**: Component logic, hooks, utilities
- **Integration tests**: Component interactions
- **E2E tests**: Complete user journeys

## Environment Variables

See `.env.example` for all available configuration options.

## Browser Support

- Chrome (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Edge (last 2 versions)
