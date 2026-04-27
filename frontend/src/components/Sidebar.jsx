import { motion } from 'framer-motion';
import { LayoutDashboard, Ticket, PenSquare, Settings, Mail, Zap } from 'lucide-react';

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'tickets', label: 'Tickets', icon: Ticket },
  { id: 'compose', label: 'Compose', icon: PenSquare },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ activePage, onNavigate }) {
  return (
    <aside style={{
      width: 264, position: 'fixed', top: 0, left: 0, bottom: 0, zIndex: 100,
      background: 'linear-gradient(180deg, #0d1117 0%, #0a0e16 100%)',
      borderRight: '1px solid var(--border)',
      display: 'flex', flexDirection: 'column',
      backdropFilter: 'blur(20px)',
    }}>
      {/* Brand */}
      <div style={{
        padding: '28px 24px', borderBottom: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', gap: 14,
      }}>
        <motion.div
          whileHover={{ rotate: 10, scale: 1.05 }}
          style={{
            width: 44, height: 44, borderRadius: 12,
            background: 'var(--gradient-brand)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 0 24px rgba(99,102,241,0.35)',
          }}
        >
          <Mail size={22} color="#fff" />
        </motion.div>
        <div>
          <h1 style={{
            fontSize: '1.15rem', fontWeight: 800, letterSpacing: '-0.02em',
            background: 'var(--gradient-brand)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          }}>MAILFLOW</h1>
          <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: 3 }}>
            AI AGENT SUITE
          </span>
        </div>
      </div>

      {/* Navigation */}
      <nav style={{ flex: 1, padding: '20px 12px', display: 'flex', flexDirection: 'column', gap: 4 }}>
        {navItems.map(item => {
          const isActive = activePage === item.id;
          const Icon = item.icon;
          return (
            <motion.button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              whileHover={{ x: 4 }}
              whileTap={{ scale: 0.98 }}
              style={{
                display: 'flex', alignItems: 'center', gap: 12,
                padding: '13px 16px', borderRadius: 'var(--radius-md)',
                background: isActive ? 'rgba(99,102,241,0.1)' : 'transparent',
                border: `1px solid ${isActive ? 'rgba(99,102,241,0.2)' : 'transparent'}`,
                color: isActive ? 'var(--accent-light)' : 'var(--text-secondary)',
                cursor: 'pointer', fontSize: '0.88rem', fontWeight: 500,
                fontFamily: 'inherit', textAlign: 'left', width: '100%',
                transition: 'var(--transition)',
                boxShadow: isActive ? '0 0 20px rgba(99,102,241,0.08)' : 'none',
              }}
            >
              <Icon size={19} />
              {item.label}
              {isActive && (
                <motion.div
                  layoutId="activeIndicator"
                  style={{
                    marginLeft: 'auto', width: 6, height: 6, borderRadius: '50%',
                    background: 'var(--accent)', boxShadow: '0 0 8px var(--accent)',
                  }}
                />
              )}
            </motion.button>
          );
        })}
      </nav>

      {/* Footer */}
      <div style={{ padding: '20px 16px', borderTop: '1px solid var(--border)' }}>
        <div style={{
          display: 'flex', alignItems: 'center', gap: 10,
          padding: '12px 14px', borderRadius: 'var(--radius-md)',
          background: 'rgba(16,185,129,0.06)', border: '1px solid rgba(16,185,129,0.15)',
        }}>
          <motion.div
            animate={{ opacity: [1, 0.3, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--green)' }}
          />
          <Zap size={14} color="var(--green)" />
          <span style={{ fontSize: '0.78rem', color: 'var(--green)', fontWeight: 500 }}>
            All Agents Online
          </span>
        </div>
      </div>
    </aside>
  );
}
