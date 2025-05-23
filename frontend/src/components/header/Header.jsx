import "./header.css"
import close_icon from "../../assets/close_icon.svg"
import menu_icon from "../../assets/mobile_menu_icon.svg"
import { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import furia_logo from "../../assets/furia_logo.png"
import { AuthProvider, AuthContext } from '../../features/auth/AuthProvider';
import PrivateRoute from '../../features/auth/PrivateRoute';
import LoginForm from '../../features/auth/LoginForm';

import DocumentUpload from '../../features/validation/DocumentUpload';
import EsportsProfile from '../../features/validation/EsportsProfile';
import BlueskyConnect from '../../features/social/BlueskyConnect';
import SocialMediaIntegration from '../../features/social/SocialMediaIntegration';
import AccountLink from "../account_link/AccountLink";


export default function Header() {
    const navigate = useNavigate();
    const tabs = [
        { name: "Associar Contas", path: "profile" },
        { name: "E-sports", path: "esports" },
        { name: "Redes Sociais", path: "social" },
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
                <img src={furia_logo} className="logo" alt="logo" onClick={() => navigate('/dashboard/profile')}/>


                {/* nav is a section that contains links to others pages */}
                <nav>
                    <img src={menu_icon} className="menu-icon" onClick={openMobileMenu} />
                    <ul className="nav-links">
                        {tabs.map((tab) => (
                            <li key={tab.path}>
                                <Link
                                    to={`/dashboard/${tab.path}`}
                                    className="li"
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
      className="button"
    >
      Logout
    </button>
  );
};