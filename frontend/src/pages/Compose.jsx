import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, CheckCircle } from 'lucide-react';

export default function Compose() {
  const [sent, setSent] = useState(false);
  const [form, setForm] = useState({ to: '', subject: '', body: '' });

  const handleSubmit = (e) => {
    e.preventDefault();
    setSent(true);
    setTimeout(() => { setSent(false); setForm({ to: '', subject: '', body: '' }); }, 3000);
  };

  const inputStyle = {
    width: '100%', padding: '14px 18px',
    background: 'var(--bg-tertiary)', border: '1px solid var(--border)',
    borderRadius: 'var(--radius-sm)', color: 'var(--text-primary)',
    fontFamily: 'Inter, sans-serif', fontSize: '0.9rem', outline: 'none',
  };

  const labelStyle = {
    display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)',
    textTransform: 'uppercase', letterSpacing: 1.5, marginBottom: 8,
  };

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <div style={{ marginBottom: 36 }}>
        <h2 style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.03em', marginBottom: 6 }}>Compose Email</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>Send a support email directly from the dashboard</p>
      </div>
      <div style={{ maxWidth: 680, background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
        <div style={{ padding: '20px 24px', borderBottom: '1px solid var(--border)' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 600 }}>New Email</h3>
        </div>
        <form onSubmit={handleSubmit} style={{ padding: 28 }}>
          <div style={{ marginBottom: 22 }}>
            <label style={labelStyle}>Recipient</label>
            <input type="email" required value={form.to} onChange={e => setForm({...form, to: e.target.value})} placeholder="recipient@example.com" style={inputStyle} />
          </div>
          <div style={{ marginBottom: 22 }}>
            <label style={labelStyle}>Subject</label>
            <input type="text" required value={form.subject} onChange={e => setForm({...form, subject: e.target.value})} placeholder="Email subject…" style={inputStyle} />
          </div>
          <div style={{ marginBottom: 28 }}>
            <label style={labelStyle}>Message</label>
            <textarea required value={form.body} onChange={e => setForm({...form, body: e.target.value})} placeholder="Write your message…" rows={6} style={{...inputStyle, resize: 'vertical', minHeight: 160}} />
          </div>
          <motion.button type="submit" whileHover={{ y: -2 }} whileTap={{ scale: 0.97 }} style={{
            padding: '14px 32px', border: 'none', borderRadius: 'var(--radius-sm)',
            background: sent ? 'var(--green)' : 'var(--gradient-brand)', color: '#fff',
            fontFamily: 'Inter, sans-serif', fontSize: '0.9rem', fontWeight: 600,
            cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 10,
            boxShadow: '0 4px 20px rgba(99,102,241,0.3)',
          }}>
            {sent ? <><CheckCircle size={18} /> Sent!</> : <><Send size={18} /> Send Email</>}
          </motion.button>
        </form>
      </div>
    </motion.div>
  );
}
