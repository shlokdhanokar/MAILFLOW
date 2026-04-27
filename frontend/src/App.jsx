import { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Tickets from './pages/Tickets';
import Compose from './pages/Compose';
import Settings from './pages/Settings';
import './styles/index.css';

const MOCK_TICKETS = [
  { id: 1, ticket_id: 'TICK-20260421-A3F1', sender: 'john.doe@gmail.com', subject: 'Cannot login to my account after password reset', category: 'Account Issue', status: 'new', created_at: '2026-04-21T10:30:00', forwarded_to: 'auth.mailflow@gmail.com', response_sent: true },
  { id: 2, ticket_id: 'TICK-20260421-B7C2', sender: 'sarah.k@outlook.com', subject: 'Double charged for April subscription', category: 'Billing Issue', status: 'new', created_at: '2026-04-21T11:15:00', forwarded_to: 'payment.mailflow@gmail.com', response_sent: true },
  { id: 3, ticket_id: 'TICK-20260421-D9E4', sender: 'mike.chen@yahoo.com', subject: 'App crashes when uploading large files', category: 'Technical Issue', status: 'new', created_at: '2026-04-21T12:00:00', forwarded_to: 'technical.mailflow@gmail.com', response_sent: true },
  { id: 4, ticket_id: 'TICK-20260422-F1A5', sender: 'emma.wilson@gmail.com', subject: 'How to upgrade my current plan?', category: 'General Inquiry', status: 'new', created_at: '2026-04-22T09:45:00', forwarded_to: 'general.mailflow@gmail.com', response_sent: false },
  { id: 5, ticket_id: 'TICK-20260422-C3B6', sender: 'alex.j@proton.me', subject: 'Two-factor authentication not working', category: 'Account Issue', status: 'new', created_at: '2026-04-22T14:20:00', forwarded_to: 'auth.mailflow@gmail.com', response_sent: true },
  { id: 6, ticket_id: 'TICK-20260423-E5D7', sender: 'lisa.park@gmail.com', subject: 'Refund request for cancelled order #4521', category: 'Billing Issue', status: 'new', created_at: '2026-04-23T08:10:00', forwarded_to: 'payment.mailflow@gmail.com', response_sent: true },
  { id: 7, ticket_id: 'TICK-20260423-G7F8', sender: 'raj.patel@company.io', subject: 'API endpoint returning 500 errors', category: 'Technical Issue', status: 'new', created_at: '2026-04-23T16:30:00', forwarded_to: 'technical.mailflow@gmail.com', response_sent: false },
  { id: 8, ticket_id: 'TICK-20260424-H9G9', sender: 'nina.s@email.com', subject: 'Need help integrating webhook', category: 'Technical Issue', status: 'new', created_at: '2026-04-24T11:00:00', forwarded_to: 'technical.mailflow@gmail.com', response_sent: true },
];

const MOCK_STATS = {
  total: 8,
  replied: 6,
  categories: { 'Technical Issue': 3, 'Billing Issue': 2, 'Account Issue': 2, 'General Inquiry': 1 },
  statuses: { 'new': 8 },
};

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');

  const renderPage = () => {
    switch (activePage) {
      case 'dashboard': return <Dashboard stats={MOCK_STATS} tickets={MOCK_TICKETS} />;
      case 'tickets': return <Tickets tickets={MOCK_TICKETS} />;
      case 'compose': return <Compose />;
      case 'settings': return <Settings />;
      default: return <Dashboard stats={MOCK_STATS} tickets={MOCK_TICKETS} />;
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar activePage={activePage} onNavigate={setActivePage} />
      <main style={{ flex: 1, marginLeft: 264, padding: '32px 40px', position: 'relative' }}>
        <div style={{
          position: 'fixed', top: 0, left: 264, right: 0, bottom: 0,
          background: 'radial-gradient(ellipse at 15% 50%, rgba(99,102,241,0.06) 0%, transparent 50%), radial-gradient(ellipse at 85% 20%, rgba(168,85,247,0.04) 0%, transparent 50%), radial-gradient(ellipse at 50% 90%, rgba(59,130,246,0.03) 0%, transparent 50%)',
          pointerEvents: 'none', zIndex: 0,
        }} />
        <div style={{ position: 'relative', zIndex: 1 }}>
          {renderPage()}
        </div>
      </main>
    </div>
  );
}
