import React from 'react';
import Navbar from '@theme-original/Navbar';
import BrowserOnly from '@docusaurus/BrowserOnly';

// Client-only component that checks auth state from localStorage
function ClientAuthenticatedContent() {
  const [authInfo, setAuthInfo] = React.useState<{ user: any; isAuthenticated: boolean } | null>(null);

  React.useEffect(() => {
    // Initialize auth state only on client
    const initializeAuth = async () => {
      try {
        // Check if we're in browser and get auth state from localStorage
        if (typeof window !== 'undefined') {
          const storedToken = localStorage.getItem('authToken');
          const storedUser = localStorage.getItem('user');

          if (storedToken && storedUser) {
            try {
              const user = JSON.parse(storedUser);
              setAuthInfo({
                user,
                isAuthenticated: true
              });
            } catch (parseError) {
              // If parsing fails, clear invalid data
              localStorage.removeItem('authToken');
              localStorage.removeItem('user');
              setAuthInfo(null);
            }
          } else {
            setAuthInfo(null);
          }
        }
      } catch (error) {
        console.warn('Auth initialization error:', error);
        setAuthInfo(null);
      }
    };

    initializeAuth();
  }, []);

  if (!authInfo || !authInfo.isAuthenticated) {
    return null;
  }

  const handleLogout = () => {
    // Clear auth data from localStorage
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    setAuthInfo(null);
    // Refresh the page to update the navbar
    window.location.reload();
  };

  return (
    <div style={{ position: 'fixed', top: 60, right: 10, backgroundColor: 'rgba(0,0,0,0.7)', color: 'white', padding: '5px 10px', borderRadius: '4px', zIndex: 1000, fontSize: '12px' }}>
      Signed in as: {authInfo.user?.email}
    </div>
  );
}

function NavbarWrapper(props) {
  return (
    <>
      <Navbar {...props} />
      <BrowserOnly>
        {() => <ClientAuthenticatedContent />}
      </BrowserOnly>
    </>
  );
}

export default NavbarWrapper;