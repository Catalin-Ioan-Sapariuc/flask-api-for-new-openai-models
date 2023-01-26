import { useState } from "react";
import { useForm } from "react-hook-form";

import axios from "axios";

interface FormData {
  prompt: string;
}

export const Prompt: React.FC = () => {
  const { register, handleSubmit, setValue } = useForm();

  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onSubmit = async (data: FormData) => {
    const { prompt } = data;

    setError(null);
    setLoading(true);

    try {
      const response = await axios.post(process.env.PROMPT_API_URL, { prompt });

      const { text } = response.data;

      setAnswers((p) => p.concat(text));
      setQuestions((p) => p.concat(prompt));

      setValue("prompt", "");
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {error && (
        <div>
          <h6>Error: {error.toString()}</h6>
        </div>
      )}

      {questions && (
        <div>
          {new Array(questions.length).fill(0).map((_, i) => {
            const question = questions[i];
            const answer = answers[i];

            return (
              <div key={i}>
                <h6>Question: {question}</h6>
                <h6>Answer: {answer}</h6>

                <hr />
              </div>
            );
          })}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)}>
        <input disabled={loading} {...register("prompt")} />

        <button style={{ marginLeft: "1em" }} disabled={loading} type="submit">
          Ask
        </button>
      </form>
    </div>
  );
};
