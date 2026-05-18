export default function EventLog({ logs }) {

  return (

    <div
      style={{
        background: '#061226',
        border: '1px solid #13233d',
        borderRadius: '22px',
        padding: '18px',
        minHeight: '650px'
      }}
    >

      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px'
        }}
      >

        <h2
          style={{
            color: '#67e8f9',
            margin: 0,
            fontSize: '22px'
          }}
        >
          Incident Log
        </h2>

        <div
          style={{
            background: '#0f172a',
            border: '1px solid #1e293b',
            padding: '10px 14px',
            borderRadius: '12px',
            color: '#94a3b8',
            fontSize: '14px'
          }}
        >
          {logs.length} Events
        </div>

      </div>

      {
        logs.map((log, index) => (

          <div
            key={index}
            style={{
              border: `1px solid ${
                log.level === 'HIGH'
                  ? '#ef4444'
                  : log.level === 'MEDIUM'
                  ? '#eab308'
                  : '#22c55e'
              }`,
              borderRadius: '18px',
              padding: '18px',
              marginBottom: '16px',
              background: '#0b1730'
            }}
          >

            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >

              <div>

                <div
                  style={{
                    fontSize: '13px',
                    color: '#67e8f9',
                    marginBottom: '12px',
                    fontWeight: 'bold'
                  }}
                >
                  {log.event}
                </div>

                <div
                  style={{
                    fontSize: '30px',
                    fontWeight: 'bold',
                    color: 'white'
                  }}
                >
                  ID {log.id}
                </div>

              </div>

              <div
                style={{
                  textAlign: 'right'
                }}
              >

                <div
                  style={{
                    fontSize: '34px',
                    fontWeight: 'bold',
                    color:
                      log.level === 'HIGH'
                        ? '#ef4444'
                        : log.level === 'MEDIUM'
                        ? '#eab308'
                        : '#22c55e'
                  }}
                >
                  {log.score}%
                </div>

                <div
                  style={{
                    marginTop: '6px',
                    fontSize: '14px',
                    fontWeight: 'bold',
                    color:
                      log.level === 'HIGH'
                        ? '#ef4444'
                        : log.level === 'MEDIUM'
                        ? '#eab308'
                        : '#22c55e'
                  }}
                >
                  {log.level} RISK
                </div>

              </div>

            </div>

          </div>

        ))
      }

    </div>

  )

}