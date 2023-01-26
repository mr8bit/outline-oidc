import { Fragment } from "react";
import { mutate } from "swr";
import { Dialog, Transition } from "@headlessui/react";
// services
import cycleService from "services/cycles.service";
// components
import { CycleForm } from "components/cycles";
// helpers
import { renderDateFormat } from "helpers/date-time.helper";
// types
import type { ICycle } from "types";
// fetch keys
import { CYCLE_LIST } from "constants/fetch-keys";

export interface CycleModalProps {
  isOpen: boolean;
  handleClose: () => void;
  projectId: string;
  workspaceSlug: string;
  initialData?: ICycle;
}

export const CycleModal: React.FC<CycleModalProps> = (props) => {
  const { isOpen, handleClose, initialData, projectId, workspaceSlug } = props;

  const createCycle = (payload: Partial<ICycle>) => {
    cycleService
      .createCycle(workspaceSlug as string, projectId, payload)
      .then((res) => {
        mutate(CYCLE_LIST(projectId));
        handleClose();
      })
      .catch((err) => {
        // TODO: Handle this ERROR.
        // Object.keys(err).map((key) => {
        //   setError(key as keyof typeof defaultValues, {
        //     message: err[key].join(", "),
        //   });
        // });
      });
  };

  const updateCycle = (cycleId: string, payload: Partial<ICycle>) => {
    cycleService
      .updateCycle(workspaceSlug, projectId, cycleId, payload)
      .then((res) => {
        mutate(CYCLE_LIST(projectId));
        handleClose();
      })
      .catch((err) => {
        // TODO: Handle this ERROR.
        //   Object.keys(err).map((key) => {
        //     setError(key as keyof typeof defaultValues, {
        //       message: err[key].join(", "),
        //     });
        //   });
      });
  };

  const handleFormSubmit = (formValues: Partial<ICycle>) => {
    if (workspaceSlug && projectId) {
      const payload = {
        ...formValues,
        start_date: formValues.start_date ? renderDateFormat(formValues.start_date) : null,
        end_date: formValues.end_date ? renderDateFormat(formValues.end_date) : null,
      };
      if (initialData) {
        updateCycle(initialData.id, payload);
      } else {
        createCycle(payload);
      }
    }
  };

  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-20" onClose={handleClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>
        <div className="fixed inset-0 z-20 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-5 py-8 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl sm:p-6">
                <Dialog.Title as="h3" className="text-lg font-medium leading-6 text-gray-900">
                  {initialData ? "Update" : "Create"} Cycle
                </Dialog.Title>
                <CycleForm handleFormSubmit={handleFormSubmit} handleFormCancel={handleClose} />
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
};