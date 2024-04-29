import { Group, ToyBrick } from "lucide-react";
import { useEffect } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
// import DropdownButton from "../../components/DropdownButtonComponent";
import IconComponent from "../../components/genericIconComponent";
import PageLayout from "../../components/pageLayout";
import SidebarNav from "../../components/sidebarComponent";
import { Button } from "../../components/ui/button";
import { USER_PROJECTS_HEADER } from "../../constants/constants";
import useAlertStore from "../../stores/alertStore";
import useFlowsManagerStore from "../../stores/flowsManagerStore";
import { downloadFlows } from "../../utils/reactflowUtils";
export default function HomePage(): JSX.Element {
  const addFlow = useFlowsManagerStore((state) => state.addFlow);
  const uploadFlow = useFlowsManagerStore((state) => state.uploadFlow);
  const setCurrentFlowId = useFlowsManagerStore(
    (state) => state.setCurrentFlowId
  );
  const uploadFlows = useFlowsManagerStore((state) => state.uploadFlows);
  const setSuccessData = useAlertStore((state) => state.setSuccessData);
  const setErrorData = useAlertStore((state) => state.setErrorData);
  const location = useLocation();
  const pathname = location.pathname;
  const is_component = pathname === "/components";
  const dropdownOptions = [
    {
      name: "Import from JSON",
      onBtnClick: () => {
        uploadFlow({
          newProject: true,
          isComponent: is_component,
        })
          .then((id) => {
            setSuccessData({
              title: `${is_component ? "Component" : "Flow"
                } uploaded successfully`,
            });
            if (!is_component) navigate("/flow/" + id);
          })
          .catch((error) => {
            setErrorData({
              title: "Error uploading file",
              list: [error],
            });
          });
      },
    },
  ];
  const sidebarNavItems = [
    {
      title: "My Datasets",
      href: "/flows",
      icon: <Group className="w-5 stroke-[1.5]" />,
    },
    {
      title: "Create Datasets",
      href: "/components",
      icon: <ToyBrick className="mx-[0.08rem] w-[1.1rem] stroke-[1.5]" />,
    },
  ];

  // Set a null id
  useEffect(() => {
    setCurrentFlowId("");
  }, [pathname]);

  const navigate = useNavigate();

  // Personal flows display
  return (
    <PageLayout
      title={"Create Datasets for your LLM model"}
      description="You can do so by clicking on the Start here button under Create Datsets"
      button={
        <div className="flex gap-2">
          <Button
            variant="primary"
            onClick={() => {
              downloadFlows();
            }}
          >
            <IconComponent name="Download" className="main-page-nav-button" />
            Download Collection
          </Button>
        </div>
      }
    >
      <div className="flex h-full w-full space-y-8 lg:flex-row lg:space-x-8 lg:space-y-0">
        <aside className="flex h-full flex-col space-y-6 lg:w-1/5">
          <SidebarNav items={sidebarNavItems} />
        </aside>
        <div className="h-full w-full flex-1">
          <Outlet />
        </div>
      </div>
    </PageLayout>
  );
}
