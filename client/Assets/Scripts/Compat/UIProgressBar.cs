using UnityEngine;
using UnityEngine.UI;

namespace DuloGames.UI
{
    // Clean-room compatibility component for the only API surface this project uses.
    [AddComponentMenu("Nexus/Compatibility/UI Progress Bar")]
    public sealed class UIProgressBar : MonoBehaviour
    {
        [SerializeField] private Image targetImage;
        [SerializeField, Range(0f, 1f)] private float currentFillAmount = 1f;

        public float fillAmount
        {
            get => currentFillAmount;
            set
            {
                currentFillAmount = Mathf.Clamp01(value);
                Apply();
            }
        }

        private void Awake()
        {
            ResolveTarget();
            Apply();
        }

        private void OnValidate()
        {
            currentFillAmount = Mathf.Clamp01(currentFillAmount);
            ResolveTarget();
            Apply();
        }

        private void ResolveTarget()
        {
            if (targetImage == null)
            {
                targetImage = GetComponent<Image>();
            }
        }

        private void Apply()
        {
            if (targetImage != null)
            {
                targetImage.fillAmount = currentFillAmount;
            }
        }
    }
}
