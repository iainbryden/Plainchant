# Species Counterpoint Generator - Frontend

React + TypeScript frontend for the Species Counterpoint Generator.

## Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Language**: TypeScript
- **HTTP Client**: Axios
- **Audio**: Tone.js
- **Notation**: VexFlow

## Project Structure

```
frontend/
├── src/
│   ├── components/    # React components
│   ├── services/      # API client
│   ├── types/         # TypeScript interfaces
│   ├── utils/         # Helper functions
│   ├── App.tsx        # Main app component
│   └── main.tsx       # Entry point
├── public/            # Static assets
└── package.json
```

## Setup

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

App runs at: `http://localhost:5173`

## Build

```bash
npm run build
```

## Environment Variables

Create `.env` file:

```
VITE_API_BASE_URL=http://localhost:8000
```

## Status

**Phase 9: Frontend Foundation** ✅ Complete
- React app scaffolded
- API service layer implemented
- TypeScript types defined
- Dependencies installed

**Next**: Phase 10 - UI Components
