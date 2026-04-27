import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Area, AreaChart, CartesianGrid } from 'recharts';
import StatCard from '../components/StatCard';

const COLORS = ['#6366f1', '#f59e0b', '#a855f7', '#10b981'];

const trafficData = [
  { day: 'Mon', emails: 12 },
  { day: 'Tue', emails: 19 },
  { day: 'Wed', emails: 8 },
  { day: 'Thu', emails: 15 },
  { day: 'Fri', emails: 22 },
  { day: 'Sat', emails: 5 },
  { day: 'Sun', emails: 3 },
];

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: 'var(--bg-tertiary)', border: '1px solid var(--border)',
      borderRadius: 'var(--radius-sm)', padding: '10px 14px',
      boxShadow: 'var(--shadow-md)',
    }}>
      <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: 4 }}>{label}</p>
      <p style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--accent-light)' }}>
        {payload[0].value} emails
      </p>
    </div>
  );
};

export default function Dashboard({ stats, tickets }) {
  const categoryData = Object.entries(stats.categories).map(([name, value]) => ({ name, value }));
  const recentTickets = tickets.slice(0, 5);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.4 }}>
      {/* Header */}
      <div style={{ marginBottom: 36 }}>
        <motion.h2
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.03em', marginBottom: 6 }}
        >
          Dashboard
        </motion.h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
          Real-time overview of your AI email support pipeline
        </p>
      </div>

      {/* Stat Cards */}
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 20, marginBottom: 32,
      }}>
        <StatCard icon="📨" label="Total Tickets" value={stats.total} color="#6366f1" delay={0} />
        <StatCard icon="🔧" label="Technical" value={stats.categories['Technical Issue'] || 0} color="#3b82f6" delay={0.1} />
        <StatCard icon="💳" label="Billing" value={stats.categories['Billing Issue'] || 0} color="#f59e0b" delay={0.2} />
        <StatCard icon="✅" label="Replied" value={stats.replied} color="#10b981" delay={0.3} />
      </div>

      {/* Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.8fr 1fr', gap: 20, marginBottom: 32 }}>
        {/* Traffic Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          style={{
            background: 'var(--bg-card)', border: '1px solid var(--border)',
            borderRadius: 'var(--radius-lg)', overflow: 'hidden',
          }}
        >
          <div style={{
            padding: '20px 24px', borderBottom: '1px solid var(--border)',
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          }}>
            <h3 style={{ fontSize: '0.95rem', fontWeight: 600 }}>Email Traffic</h3>
            <span style={{
              fontSize: '0.72rem', padding: '4px 10px', borderRadius: 20,
              background: 'rgba(99,102,241,0.1)', color: 'var(--accent-light)', fontWeight: 500,
            }}>Last 7 days</span>
          </div>
          <div style={{ padding: '20px 16px', height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trafficData}>
                <defs>
                  <linearGradient id="colorEmails" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366f1" stopOpacity={0.3} />
                    <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(99,102,241,0.06)" />
                <XAxis dataKey="day" stroke="#484f58" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#484f58" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="emails" stroke="#6366f1" strokeWidth={2.5} fill="url(#colorEmails)" dot={{ fill: '#6366f1', r: 4, strokeWidth: 2, stroke: '#0d1117' }} activeDot={{ r: 6, stroke: '#6366f1', strokeWidth: 2 }} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Category Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          style={{
            background: 'var(--bg-card)', border: '1px solid var(--border)',
            borderRadius: 'var(--radius-lg)', overflow: 'hidden',
          }}
        >
          <div style={{ padding: '20px 24px', borderBottom: '1px solid var(--border)' }}>
            <h3 style={{ fontSize: '0.95rem', fontWeight: 600 }}>Category Breakdown</h3>
          </div>
          <div style={{ padding: '20px', height: 300, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <ResponsiveContainer width="100%" height="70%">
              <PieChart>
                <Pie data={categoryData} cx="50%" cy="50%" innerRadius={55} outerRadius={85} paddingAngle={4} dataKey="value" stroke="none">
                  {categoryData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
            <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', justifyContent: 'center' }}>
              {categoryData.map((item, i) => (
                <div key={item.name} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <div style={{ width: 8, height: 8, borderRadius: 2, background: COLORS[i] }} />
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>{item.name.replace(' Issue','').replace(' Inquiry','')}</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Recent Tickets */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        style={{
          background: 'var(--bg-card)', border: '1px solid var(--border)',
          borderRadius: 'var(--radius-lg)', overflow: 'hidden',
        }}
      >
        <div style={{ padding: '20px 24px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 600 }}>Recent Activity</h3>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Latest {recentTickets.length} tickets</span>
        </div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                {['Ticket', 'Sender', 'Subject', 'Category', 'Replied'].map(h => (
                  <th key={h} style={{
                    textAlign: 'left', padding: '14px 16px', fontSize: '0.7rem',
                    textTransform: 'uppercase', letterSpacing: 1.5, color: 'var(--text-muted)',
                    borderBottom: '1px solid var(--border)', fontWeight: 600,
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {recentTickets.map((t, i) => (
                <motion.tr
                  key={t.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 + i * 0.05 }}
                  style={{ borderBottom: '1px solid rgba(99,102,241,0.04)' }}
                  onMouseEnter={e => e.currentTarget.style.background = 'rgba(99,102,241,0.03)'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                >
                  <td style={{ padding: '14px 16px', fontSize: '0.85rem', fontWeight: 600, color: 'var(--accent-light)' }}>{t.ticket_id}</td>
                  <td style={{ padding: '14px 16px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{t.sender}</td>
                  <td style={{ padding: '14px 16px', fontSize: '0.85rem', color: 'var(--text-secondary)', maxWidth: 260, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{t.subject}</td>
                  <td style={{ padding: '14px 16px' }}>
                    <CategoryBadge category={t.category} />
                  </td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{
                      padding: '4px 12px', borderRadius: 20, fontSize: '0.72rem', fontWeight: 600,
                      background: t.response_sent ? 'rgba(16,185,129,0.1)' : 'rgba(244,63,94,0.1)',
                      color: t.response_sent ? 'var(--green)' : 'var(--rose)',
                    }}>{t.response_sent ? 'Sent' : 'Pending'}</span>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </motion.div>
  );
}

function CategoryBadge({ category }) {
  const map = {
    'Technical Issue': { bg: 'rgba(59,130,246,0.1)', color: '#3b82f6' },
    'Billing Issue': { bg: 'rgba(245,158,11,0.1)', color: '#f59e0b' },
    'Account Issue': { bg: 'rgba(168,85,247,0.1)', color: '#a855f7' },
    'General Inquiry': { bg: 'rgba(16,185,129,0.1)', color: '#10b981' },
  };
  const s = map[category] || map['General Inquiry'];
  return (
    <span style={{
      padding: '4px 12px', borderRadius: 20, fontSize: '0.72rem', fontWeight: 600,
      background: s.bg, color: s.color,
    }}>{category}</span>
  );
}
