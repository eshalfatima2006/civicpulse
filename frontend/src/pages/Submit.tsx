import { FormEvent, useState } from "react";

import { Complaint, postComplaint } from "../api/client";

const initialForm = { text: "", location: "", reporter_contact: "" };

type FormState = typeof initialForm;

function validate(form: FormState): string | null {
  if (form.text.trim().length < 10 || form.text.trim().length > 2000) {
    return "Complaint must be between 10 and 2000 characters.";
  }
  if (form.location.trim().length < 3 || form.location.trim().length > 200) {
    return "Location must be between 3 and 200 characters.";
  }
  return null;
}

export default function Submit() {
  const [form, setForm] = useState<FormState>(initialForm);
  const [complaint, setComplaint] = useState<Complaint | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  function updateField(field: keyof FormState, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
    setError(null);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const validationError = validate(form);
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsSubmitting(true);
    setError(null);
    setComplaint(null);
    try {
      const result = await postComplaint({
        text: form.text.trim(),
        location: form.location.trim(),
        ...(form.reporter_contact.trim() && { reporter_contact: form.reporter_contact.trim() }),
      });
      setComplaint(result);
    } catch (submissionError) {
      setError(submissionError instanceof Error ? submissionError.message : "Unable to submit complaint.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="intro">
        <p className="eyebrow">CivicPulse / public works</p>
        <h1>Make your neighborhood heard.</h1>
        <p className="lede">Tell us what needs attention. We’ll classify your report and route it to the right team.</p>
      </section>

      <section className="form-panel" aria-labelledby="form-title">
        <div className="panel-heading">
          <h2 id="form-title">Report an issue</h2>
          <span className="step">01 / 01</span>
        </div>
        <form onSubmit={handleSubmit} noValidate>
          <label htmlFor="complaint">What happened?</label>
          <textarea
            id="complaint"
            value={form.text}
            minLength={10}
            maxLength={2000}
            onChange={(event) => updateField("text", event.target.value)}
            placeholder="Describe the issue, including anything that could help us locate or understand it."
            required
          />
          <div className="field-meta"><span>Minimum 10 characters</span><span>{form.text.length} / 2000</span></div>

          <label htmlFor="location">Where is it?</label>
          <input
            id="location"
            value={form.location}
            minLength={3}
            maxLength={200}
            onChange={(event) => updateField("location", event.target.value)}
            placeholder="Street, landmark, or neighborhood"
            required
          />

          <label htmlFor="contact">How can we reach you? <span>(optional)</span></label>
          <input
            id="contact"
            value={form.reporter_contact}
            onChange={(event) => updateField("reporter_contact", event.target.value)}
            placeholder="Email or phone number"
          />

          {error && <p className="message error" role="alert">{error}</p>}
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Triaging..." : "Submit report"}
          </button>
        </form>
      </section>

      {complaint && (
        <section className="result-panel" aria-live="polite">
          <p className="eyebrow">Report received</p>
          <h2>Here’s what we found.</h2>
          <p className="summary">{complaint.ai_summary}</p>
          <dl className="result-grid">
            <div><dt>Category</dt><dd>{complaint.category}</dd></div>
            <div><dt>Priority</dt><dd>{complaint.priority}</dd></div>
            <div><dt>Triaged by</dt><dd>{complaint.triaged_by}</dd></div>
          </dl>
        </section>
      )}
    </main>
  );
}
