export default function VideoPanel({ title, src }) {
  return (
    <div className="bg-[#0d1b2a] border border-[#1b263b] rounded-xl p-4 flex-1">
      <h2 className="text-lg font-bold text-cyan-400 mb-4">
        {title}
      </h2>

      <div className="bg-black rounded-lg overflow-hidden h-[350px] flex items-center justify-center">
        {src ? (
          <img
            src={src}
            alt="feed"
            className="w-full h-full object-contain"
          />
        ) : (
          <p className="text-gray-500">No Feed</p>
        )}
      </div>
    </div>
  )
}