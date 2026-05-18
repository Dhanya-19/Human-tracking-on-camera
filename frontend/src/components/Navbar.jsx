export default function Navbar() {

  return (

    <div
      style={{
        width: '100%',
        padding: '22px 28px',
        borderRadius: '22px',
        background: 'linear-gradient(135deg, #081224, #0f172a)',
        border: '1px solid #1e293b',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        boxShadow: '0 0 40px rgba(0,255,255,0.06)'
      }}
    >

      <div>

        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}
        >

          <div
            style={{
              width: '14px',
              height: '14px',
              borderRadius: '50%',
              background: '#22c55e',
              boxShadow: '0 0 18px #22c55e'
            }}
          />

          <h1
            style={{
              margin: 0,
              fontSize: '34px',
              color: '#67e8f9',
              letterSpacing: '1px'
            }}
          >
            VIDEO SURVEILLANCE SYSTEM
          </h1>

        </div>

        <p
          style={{
            marginTop: '8px',
            color: '#94a3b8',
            fontSize: '15px'
          }}
        >
          Real-Time AI Surveillance Dashboard
        </p>

      </div>

      <div
        style={{
          display: 'flex',
          gap: '14px'
        }}
      >

        <div
          style={{
            background: '#0f172a',
            border: '1px solid #1e293b',
            padding: '14px 20px',
            borderRadius: '16px',
            minWidth: '120px'
          }}
        >

          <div
            style={{
              fontSize: '12px',
              color: '#94a3b8',
              letterSpacing: '1px'
            }}
          >
            STATUS
          </div>

          <div
            style={{
              color: '#22c55e',
              fontWeight: 'bold',
              marginTop: '6px',
              fontSize: '16px'
            }}
          >
            ACTIVE
          </div>

        </div>

        <div
          style={{
            background: '#0f172a',
            border: '1px solid #1e293b',
            padding: '14px 20px',
            borderRadius: '16px',
            minWidth: '160px'
          }}
        >

          <div
            style={{
              fontSize: '12px',
              color: '#94a3b8',
              letterSpacing: '1px'
            }}
          >
            MODEL
          </div>

          <div
            style={{
              color: '#67e8f9',
              fontWeight: 'bold',
              marginTop: '6px',
              fontSize: '16px'
            }}
          >
            YOLOv8 Tracking
          </div>

        </div>

      </div>

    </div>
  )
}