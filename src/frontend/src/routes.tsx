import { useEffect } from "react";
import { Route, Routes, useNavigate } from "react-router-dom";
import { ProtectedAdminRoute } from "./components/authAdminGuard";
import { CatchAllRoute } from "./components/catchAllRoutes";
import { StoreGuard } from "./components/storeGuard";
import AdminPage from "./pages/AdminPage";
import LoginAdminPage from "./pages/AdminPage/LoginPage";
import ApiKeysPage from "./pages/ApiKeysPage";
import FlowPage from "./pages/FlowPage";
import HomePage from "./pages/MainPage";
import ComponentsComponent from "./pages/MainPage/components/components";
import ProfileSettingsPage from "./pages/ProfileSettingsPage";
import ViewPage from "./pages/ViewPage";
import DeleteAccountPage from "./pages/deleteAccountPage";

const Router = () => {
  const navigate = useNavigate();
  useEffect(() => {
    // Redirect from root to /flows
    if (window.location.pathname === "/") {
      navigate("/flows");
    }
  }, [navigate]);
  return (
    <Routes>
      <Route
        path="/"
        element={
          <HomePage />
        }
      >
        <Route
          path="flows"
          element={<ComponentsComponent key="flows" is_component={false} />}
        />
        <Route
          path="components"
          element={<ComponentsComponent key="components" />}
        />
      </Route>



      <Route path="/flow/:id/">
        <Route
          path=""
          element={
            <FlowPage />
          }
        />
        <Route
          path="view"
          element={
            <ViewPage />
          }
        />
      </Route>
      <Route
        path="/admin"
        element={
          <ProtectedAdminRoute>
            <AdminPage />
          </ProtectedAdminRoute>
        }
      />

      <Route path="/account">
        <Route
          path="settings"
          element={
            <ProfileSettingsPage />
          }
        />

        <Route
          path="api-keys"
          element={
            <ApiKeysPage />
          }
        ></Route>
      </Route>
    </Routes>
  );
};

export default Router;
