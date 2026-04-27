import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, RefreshCw } from 'lucide-react';

function CategoryBadge({ category }) {
  const map = {
    'Technical Issue': { bg: 'rgba(59,130,246,0.1)', color: '#3b82f6' },
    'Billing Issue': { bg: 'rgba(245,158,11,0.1)', color: '#f59e0b' },
    'Account Issue': { bg: 'rgba(168,85,247,0.1)', color: '#a855f7' },
    'General Inquiry': { bg: 'rgba(16,185,129,0.1)', color: '#10b981' },
  };
  const s = map[category] || map['General Inquiry'];
  return (
    <span style={{ padding: '4px 12px', borderRadius: 20, fontSize: '0.72rem', fontWeight: 600, background: s.bg, color: s.color }}>
      {category}
    </span>
  );
}

export default function Tickets({ tickets }) {
  const [search, setSearch] = useState('');
  const [catFilter, setCatFilter] = useState('');

  const filtered = tickets.filter(t => {
    if (catFilter && t.category !== catFilter) return false;
    if (search) {
      const q = search.toLowerCase();
      return t.ticket_id.toLowerCase().includes(q) || t.sender.toLowerCase().includes(q) || t.subject.toLowerCase().includes(q);
    }
    return true;
  });

  const selectStyle = {
    padding: '10px 16px', borderRadius: 'var(--radius-sm)',
    background: 'var(--bg-tertiary)', border: '1px solid var(--border)',
    color: 'var(--text-primary)', fontFamily: 'Inter, sans-serif',
    fontSize: '0.85rem', outline: 'none', cursor: 'pointer',
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.4 }}>
      <div style={{ marginBottom: 36 }}>
        <h2 style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.03em', marginBottom: 6 }}>Ticket Logs</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>Browse and filter all support tickets processed by the AI agents</p>
      </div>

      <div style={{
        background: 'var(--bg-card)', border: '1px solid var(--border)',
        borderRadius: 'var(--radius-lg)', overflow: 'hidden',
      }}>
        {/* Toolbar */}
        <div style={{
          padding: '16px 24px', borderBottom: '1px solid var(--border)',
          display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap',
        }}>
          <div style={{ position: 'relative', flex: 1, minWidth: 200 }}>
            <Search size={16} style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            <input
              value={search} onChange={e => setSearch(e.target.value)}
              placeholder="Search tickets…"
              style={{ ...selectStyle, width: '100%', paddingLeft: 40 }}
            />
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <Filter size={15} color="var(--text-muted)" />
            <select value={catFilter} onChange={e => setCatFilter(e.target.value)} style={selectStyle}>
              <option value="">All Categories</option>
              <option value="Technical Issue">Technical</option>
              <option value="Billing Issue">Billing</option>
              <option value="Account Issue">Account</option>
              <option value="General Inquiry">General</option>
            </select>
          </div>
          <motion.button
            whileHover={{ rotate: 180 }}
            transition={{ duration: 0.4 }}
            style={{
              width: 40, height: 40, borderRadius: 'var(--radius-sm)',
              background: 'var(--bg-tertiary)', border: '1px solid var(--border)',
              color: 'var(--text-secondary)', cursor: 'pointer',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}
          >
            <RefreshCw size={16} />
          </motion.button>
        </div>

        {/* Table */}
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                {['Ticket ID', 'Sender', 'Subject', 'Category', 'Status', 'Date', 'Replied'].map(h => (
                  <th key={h} style={{
                    textAlign: 'left', padding: '14px 16px', fontSize: '0.7rem',
                    textTransform: 'uppercase', letterSpacing: 1.5, color: 'var(--text-muted)',
                    borderBottom: '1px solid var(--border)', fontWeight: 600,
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: 60, color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                    No tickets match your filters
                  </td>
                </tr>
              ) : filtered.map((t, i) => (
                <motion.tr
                  key={t.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: i * 0.03 }}
                  style={{ borderBottom: '1px solid rgba(99,102,241,0.04)', cursor: 'default' }}
                  onMouseEnter={e => e.currentTarget.style.background = 'rgba(99,102,241,0.03)'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                >
                  <td style={{ padding: '14px 16px', fontSize: '0.85rem', fontWeight: 600, color: 'var(--accent-light)' }}>{t.ticket_id}</td>
                  <td style={{ padding: '14px 16px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{t.sender}</td>
                  <td style={{ padding: '14px 16px', fontSize: '0.85rem', color: 'var(--text-secondary)', maxWidth: 300, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{t.subject}</td>
                  <td style={{ padding: '14px 16px' }}><CategoryBadge category={t.category} /></td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{
                      padding: '4px 12px', borderRadius: 20, fontSize: '0.72rem', fontWeight: 600,
                      background: 'rgba(99,102,241,0.1)', color: 'var(--accent-light)',
                    }}>{t.status}</span>
                  </td>
                  <td style={{ padding: '14px 16px', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    {new Date(t.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{
                      padding: '4px 12px', borderRadius: 20, fontSize: '0.72rem', fontWeight: 600,
                      background: t.response_sent ? 'rgba(16,185,129,0.1)' : 'rgba(244,63,94,0.1)',
                      color: t.response_sent ? '#10b981' : '#f43f5e',
                    }}>{t.response_sent ? 'Sent' : 'Pending'}</span>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div style={{ padding: '14px 24px', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Showing {filtered.length} of {tickets.length} tickets
          </span>
        </div>
      </div>
    </motion.div>
  );
}
