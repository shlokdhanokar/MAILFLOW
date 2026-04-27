import { motion } from 'framer-motion';
import { Mail, Brain, Shield } from 'lucide-react';

const deptEmails = [
  { label: 'Technical Issue', email: 'technical.mailflow@gmail.com', color: '#3b82f6' },
  { label: 'Billing Issue', email: 'payment.mailflow@gmail.com', color: '#f59e0b' },
  { label: 'Account Issue', email: 'auth.mailflow@gmail.com', color: '#a855f7' },
  { label: 'General Inquiry', email: 'general.mailflow@gmail.com', color: '#10b981' },
];

const aiModels = [
  { label: 'Email Classifier', value: 'BERT (fine-tuned)', icon: '🧠' },
  { label: 'Reply Generator', value: 'Gemini 1.5 Flash', icon: '✨' },
  { label: 'Categories', value: '4 classes', icon: '📊' },
  { label: 'Max Token Length', value: '512 tokens', icon: '📏' },
];

const agents = [
  { name: 'EmailFetcher', desc: 'Connects to Gmail IMAP and fetches unread emails', status: 'Online' },
  { name: 'Classifier', desc: 'Categorizes emails using BERT model', status: 'Online' },
  { name: 'Database', desc: 'Stores tickets and logs in MySQL', status: 'Online' },
  { name: 'Forwarder', desc: 'Routes emails to correct department via Flask API', status: 'Online' },
  { name: 'Replier', desc: 'Generates AI replies using Google Gemini', status: 'Online' },
];

export default function Settings() {
  const cardStyle = {
    background: 'var(--bg-card)', border: '1px solid var(--border)',
    borderRadius: 'var(--radius-lg)', overflow: 'hidden',
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div style={{ marginBottom: 36 }}>
        <h2 style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.03em', marginBottom: 6 }}>Settings</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>System configuration, agent status, and department mappings</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 24 }}>
        {/* Department Emails */}
        <div style={cardStyle}>
          <div style={{ padding: '20px 24px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: 10 }}>
            <Mail size={18} color="var(--accent-light)" />
            <h3 style={{ fontSize: '0.95rem', fontWeight: 600 }}>Department Emails</h3>
          </div>
          <div style={{ padding: '8px 24px' }}>
            {deptEmails.map(d => (
              <div key={d.label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '14px 0', borderBottom: '1px solid rgba(99,102,241,0.04)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <div style={{ width: 8, height: 8, borderRadius: 2, background: d.color }} />
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{d.label}</span>
                </div>
                <code style={{ fontSize: '0.8rem', color: 'var(--text-primary)', background: 'var(--bg-tertiary)', padding: '4px 10px', borderRadius: 6 }}>{d.email}</code>
              </div>
            ))}
          </div>
        </div>

        {/* AI Models */}
        <div style={cardStyle}>
          <div style={{ padding: '20px 24px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: 10 }}>
            <Brain size={18} color="var(--accent-light)" />
            <h3 style={{ fontSize: '0.95rem', fontWeight: 600 }}>AI Model Configuration</h3>
          </div>
          <div style={{ padding: '8px 24px' }}>
            {aiModels.map(m => (
              <div key={m.label} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '14px 0', borderBottom: '1px solid rgba(99,102,241,0.04)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span>{m.icon}</span>
                  <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{m.label}</span>
                </div>
                <code style={{ fontSize: '0.8rem', color: 'var(--text-primary)', background: 'var(--bg-tertiary)', padding: '4px 10px', borderRadius: 6 }}>{m.value}</code>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Agent Status */}
      <div style={cardStyle}>
        <div style={{ padding: '20px 24px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: 10 }}>
          <Shield size={18} color="var(--accent-light)" />
          <h3 style={{ fontSize: '0.95rem', fontWeight: 600 }}>Agent Status</h3>
        </div>
        <div style={{ padding: '8px 24px' }}>
          {agents.map((a, i) => (
            <motion.div
              key={a.name}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.08 }}
              style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '14px 0', borderBottom: '1px solid rgba(99,102,241,0.04)' }}
            >
              <div>
                <p style={{ fontSize: '0.88rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: 2 }}>{a.name}</p>
                <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{a.desc}</p>
              </div>
              <span style={{ padding: '4px 12px', borderRadius: 20, fontSize: '0.72rem', fontWeight: 600, background: 'rgba(16,185,129,0.1)', color: '#10b981' }}>{a.status}</span>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
