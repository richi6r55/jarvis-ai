import React from 'react';

function Sidebar({ isOpen, onToggle }) {
  return (
    <div
      className={`${
        isOpen ? 'w-64' : 'w-20'
      } bg-gray-900 text-white transition-all duration-300 flex flex-col`}
    >
      {/* Logo */}
      <div className="p-4 flex items-center justify-between">
        {isOpen && <h1 className="text-xl font-bold">JARVIS</h1>}
        <button
          onClick={onToggle}
          className="p-2 hover:bg-gray-800 rounded-lg"
        >
          {isOpen ? '←' : '→'}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        <NavItem icon="💬" label="Chat" isOpen={isOpen} active={true} />
        <NavItem icon="🎮" label="PC Control" isOpen={isOpen} />
        <NavItem icon="🌐" label="Browser" isOpen={isOpen} />
        <NavItem icon="🏠" label="Smart Home" isOpen={isOpen} />
        <NavItem icon="📞" label="Twilio" isOpen={isOpen} />
      </nav>

      {/* Settings */}
      <div className="p-4 border-t border-gray-700">
        <NavItem icon="⚙️" label="Settings" isOpen={isOpen} />
      </div>
    </div>
  );
}

function NavItem({ icon, label, isOpen, active = false }) {
  return (
    <button
      className={`w-full flex items-center gap-3 p-3 rounded-lg transition ${
        active
          ? 'bg-blue-500'
          : 'hover:bg-gray-800'
      }`}
    >
      <span className="text-xl">{icon}</span>
      {isOpen && <span>{label}</span>}
    </button>
  );
}

export default Sidebar;
