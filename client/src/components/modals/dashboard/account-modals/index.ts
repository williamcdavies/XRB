import ChangePictureModal from './ChangePictureModal.vue'
import ChangeNameModal from './ChangeNameModal.vue'
import ChangeAccountTypeModal from './ChangeAccountTypeModal.vue'
import ChangeLanguageModal from './ChangeLanguageModal.vue'
import ChangeEmailModal from './ChangeEmailModal.vue'
import DeleteAccountModal from './DeleteAccountModal.vue'

export const accountModals = {
    picture: ChangePictureModal,
    name: ChangeNameModal,
    type: ChangeAccountTypeModal,
    language: ChangeLanguageModal,
    email: ChangeEmailModal,
    delete: DeleteAccountModal
} as const

export type AccountModalType = keyof typeof accountModals