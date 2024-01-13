import { post } from "../gateway";
import Base from "./Base";

export default class Member extends Base {
    deleteConfirmMessage() {
        return `Are you sure you want to delete member ${this.firstname} ${this.lastname}?`;
    }

    save() {
        if (Object.prototype.hasOwnProperty.call(this.unsaved, "email")) {
            post({
                url: "/member/send_updated_member_info",
                data: {
                    member_id: this.member_id,
                    msg_swe: `Din epost ändrades från ${this.saved.email} till ${this.unsaved.email}`,
                    msg_en: `Your email was updated from ${this.saved.email} to ${this.unsaved.email}`,
                },
                errorMessage:
                    "Error when sending email about updated information.",
                expectedDataStatus: "ok",
            });
        }
        super.save();
    }

    canSave() {
        return (
            this.isDirty() &&
            this.firstname.length > 0 &&
            this.email.length > 0 &&
            this.email.includes("@") &&
            this.email.includes(".")
        );
    }
}

Member.model = {
    id: "member_id",
    root: "/membership/member",
    attributes: {
        member_id: 0,
        created_at: null,
        updated_at: null,
        member_number: null,
        civicregno: "",
        firstname: "",
        lastname: "",
        email: "",
        phone: "",
        address_street: "",
        address_extra: "",
        address_zipcode: null,
        address_city: "",
        address_country: "se",
        labaccess_agreement_at: null,
        pending_activation: false,
        price_level: "normal",
    },
};
