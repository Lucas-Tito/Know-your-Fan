import "./header.css"
import close_icon from "../../assets/close_icon.svg"
import menu_icon from "../../assets/mobile_menu_icon.svg"
import { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';

import { AuthProvider, AuthContext } from '../../features/auth/AuthProvider';
import PrivateRoute from '../../features/auth/PrivateRoute';
import LoginForm from '../../features/auth/LoginForm';

import DocumentUpload from '../../features/validation/DocumentUpload';
import EsportsProfile from '../../features/validation/EsportsProfile';
import BlueskyConnect from '../../features/social/BlueskyConnect';
import SocialMediaIntegration from '../../features/social/SocialMediaIntegration';
import AccountLink from "../account_link/AccountLink";


export default function Header() {

    const tabs = [
        { name: "Associar Contas", path: "profile" },
        { name: "E-sports", path: "esports" },
        { name: "Redes Sociais", path: "social" },
        { name: "Bluesky", path: "bluesky" }
    ];


    const openMobileMenu = () => {
        let mobile_menu = document.querySelector(".mobile_menu")
        mobile_menu.classList.toggle("active")
    }

    const closeMobileMenu = () => {
        let mobile_menu = document.querySelector(".mobile_menu")
        mobile_menu.classList.remove("active")
    }

    const goTo = (location) => {
        closeMobileMenu()
        window.location.href = `${location}`
    }

    // closes mobile menu when user uses go back on the system rather than the close btn
    window.addEventListener('popstate', closeMobileMenu);
    return (
        <>
            {/* header represents a support tag that can work as a navigation section */}
            <header>
                <span className="logo" alt="logo" onClick={console.log("logo")}>
                    Lucas Tito
                </span>


                {/* nav is a section that contains links to others pages */}
                <nav>
                    <img src={menu_icon} className="menu-icon" onClick={openMobileMenu} />
                    <ul className="nav-links">
                        {tabs.map((tab) => (
                            <li key={tab.path}>
                                <Link
                                    to={`/dashboard/${tab.path}`}
                                >
                                    {tab.name}
                                </Link>
                            </li>
                        ))}
                        <LogoutButton />
                    </ul>
                </nav>
            </header>

            <div className="mobile_menu">
                <img src={close_icon} className="close_btn" onClick={closeMobileMenu} />
                <ul className="menu_links">
                    <li onClick={() => goTo("#home")}>Home</li>
                    <li onClick={() => goTo("#about")}>About</li>
                    <li onClick={() => goTo("#portfolio")}>Projects</li>
                    <li onClick={() => goTo("#contact")}>Contact</li>
                </ul>
            </div>

            <main className="py-6 px-4">
                <Routes>
                    <Route path="profile" element={<AccountLink />} />
                    <Route path="esports" element={<EsportsProfile />} />
                    <Route path="social" element={<SocialMediaIntegration />} />
                    <Route path="bluesky" element={<BlueskyConnect />} />
                    <Route path="*" element={<Navigate to="profile" replace />} />
                </Routes>
            </main>
        </>

    )
}


const LogoutButton = () => {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  return (
    <button
      onClick={handleLogout}
      className="px-4 py-2 bg-red-600 rounded hover:bg-red-700 transition"
    >
      Logout
    </button>
  );
};