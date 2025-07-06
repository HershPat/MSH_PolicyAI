import './ChatHeader.css';
export default function ChatHeader({title, user}) {
    return (
        <header className=" text-white p-4 flex justify-between items-center border-zinc-400 pb-5 border-b-2 ">
            <h1 className="text-xl font-bold">{title}</h1>
            <div className="flex items-center space-x-4">
                <span className="text-sm font-bold hover:bg-gray-800">{user}</span>
                <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Logout
                </button>
            </div>
        </header>
    );
}