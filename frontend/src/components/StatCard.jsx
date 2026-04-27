import { motion } from 'framer-motion';

export default function StatCard({ icon, label, value, color, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ y: -6, boxShadow: '0 0 40px rgba(99,102,241,0.12)' }}
      style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: 'var(--radius-lg)',
        padding: '28px 24px',
        backdropFilter: 'blur(16px)',
        position: 'relative',
        overflow: 'hidden',
        cursor: 'default',
        transition: 'var(--transition)',
      }}
    >
      {/* Top accent line */}
      <div style={{
        position: 'absolute', top: 0, left: 0, right: 0, height: 2,
        background: `linear-gradient(90deg, ${color}, transparent)`,
        opacity: 0.6,
      }} />

      {/* Icon */}
      <div style={{
        position: 'absolute', top: 20, right: 20,
        width: 48, height: 48, borderRadius: 14,
        background: `${color}12`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '1.3rem',
      }}>
        {icon}
      </div>

      {/* Label */}
      <p style={{
        fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-muted)',
        textTransform: 'uppercase', letterSpacing: 1.8, marginBottom: 10,
      }}>
        {label}
      </p>

      {/* Value */}
      <motion.p
        initial={{ scale: 0.5 }}
        animate={{ scale: 1 }}
        transition={{ type: 'spring', stiffness: 200, delay: delay + 0.2 }}
        style={{
          fontSize: '2.5rem', fontWeight: 900, letterSpacing: '-0.03em',
          background: `linear-gradient(135deg, ${color}, ${color}99)`,
          WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          lineHeight: 1.1,
        }}
      >
        {value}
      </motion.p>

      {/* Subtle glow */}
      <div style={{
        position: 'absolute', bottom: -40, left: -20,
        width: 120, height: 120, borderRadius: '50%',
        background: `radial-gradient(circle, ${color}08 0%, transparent 70%)`,
      }} />
    </motion.div>
  );
}
