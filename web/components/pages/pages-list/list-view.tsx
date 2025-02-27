import { FC } from "react";
import { useRouter } from "next/router";
import { Plus } from "lucide-react";
// hooks
import { useApplication, useUser } from "hooks/store";
// components
import { NewEmptyState } from "components/common/new-empty-state";
// ui
import { Loader } from "@plane/ui";
// images
import emptyPage from "public/empty-state/empty_page.png";
// constants
import { EUserProjectRoles } from "constants/project";
import { PagesListItem } from "./list-item";

type IPagesListView = {
  pageIds: string[];
};

export const PagesListView: FC<IPagesListView> = (props) => {
  const { pageIds: projectPageIds } = props;
  // store hooks
  // trace(true);

  const {
    commandPalette: { toggleCreatePageModal },
  } = useApplication();
  const {
    membership: { currentProjectRole },
  } = useUser();
  // router
  const router = useRouter();
  const { workspaceSlug, projectId } = router.query;

  // here we are only observing the projectPageStore, so that we can re-render the component when the projectPageStore changes

  const isEditingAllowed = !!currentProjectRole && currentProjectRole >= EUserProjectRoles.MEMBER;

  return (
    <>
      {projectPageIds && workspaceSlug && projectId ? (
        <div className="h-full space-y-4 overflow-y-auto">
          {projectPageIds.length > 0 ? (
            <ul role="list" className="divide-y divide-custom-border-200">
              {projectPageIds.map((pageId: string) => (
                <PagesListItem key={pageId} pageId={pageId} projectId={projectId.toString()} />
              ))}
            </ul>
          ) : (
            <NewEmptyState
              title="Write a note, a doc, or a full knowledge base. Get Galileo, Plane’s AI assistant, to help you get started."
              description="Pages are thoughtspotting space in Plane. Take down meeting notes, format them easily, embed issues, lay them out using a library of components, and keep them all in your project’s context. To make short work of any doc, invoke Galileo, Plane’s AI, with a shortcut or the click of a button."
              image={emptyPage}
              comicBox={{
                title: "A page can be a doc or a doc of docs.",
                description:
                  "We wrote Parth and Meera’s love story. You could write your project’s mission, goals, and eventual vision.",
                direction: "right",
              }}
              primaryButton={{
                icon: <Plus className="h-4 w-4" />,
                text: "Create your first page",
                onClick: () => toggleCreatePageModal(true),
              }}
              disabled={!isEditingAllowed}
            />
          )}
        </div>
      ) : (
        <Loader className="space-y-4">
          <Loader.Item height="40px" />
          <Loader.Item height="40px" />
          <Loader.Item height="40px" />
        </Loader>
      )}
    </>
  );
};
