export default function StatsCard({ title, value, color }) {

  return (

    <div
      style={{
        background: '#081224',
        border: '1px solid #1e293b',
        borderRadius: '22px',
        padding: '24px',
        flex: 1,
        position: 'relative',
        overflow: 'hidden'
      }}
    >

      <div
        style={{
          position: 'absolute',
          top: '-40px',
          right: '-40px',
          width: '120px',
          height: '120px',
          borderRadius: '50%',
          background: color,
          opacity: 0.08
        }}
      />

      <div
        style={{
          color: '#94a3b8',
          fontSize: '13px',
          letterSpacing: '1px'
        }}
      >
        {title}
      </div>

      <div
        style={{
          marginTop: '16px',
          fontSize: '42px',
          fontWeight: 'bold'
        }}
      >
        {value}
      </div>

    </div>
  )
}